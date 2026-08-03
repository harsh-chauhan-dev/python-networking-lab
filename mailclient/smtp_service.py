import os
import smtplib
import mimetypes
from email.message import EmailMessage
from email.utils import formataddr
from typing import Optional, List, Dict, Any, Tuple
from config import Config
from template_service import TemplateService


class EmailService:
    """Service handling SMTP email operations."""

    def __init__(self):
        self.config = Config()

    def test_connection(self) -> Tuple[bool, str]:
        """Tests SMTP connection and login credentials."""
        valid, msg = self.config.validate()
        if not valid:
            return False, msg

        try:
            with smtplib.SMTP(self.config.SMTP_SERVER, self.config.SMTP_PORT, timeout=10) as smtp:
                smtp.starttls()
                smtp.login(self.config.EMAIL, self.config.PASSWORD)
            return True, "SMTP connection and authentication successful!"
        except Exception as err:
            return False, f"SMTP Connection Failed: {err}"

    def send_email(
        self,
        receiver: str,
        subject: str,
        body_text: str,
        body_html: Optional[str] = None,
        attachment_path: Optional[str] = None,
    ) -> bool:
        """Sends an email (plain text and/or HTML) with optional attachment."""
        valid, msg = self.config.validate()
        if not valid:
            print(f" Configuration error: {msg}")
            return False

        message = EmailMessage()
        if self.config.FROM_NAME:
            message["From"] = formataddr((self.config.FROM_NAME, self.config.EMAIL))
        else:
            message["From"] = self.config.EMAIL

        message["To"] = receiver
        message["Subject"] = subject

        # Set plain-text content
        message.set_content(body_text)

        # Add HTML alternative if provided
        if body_html:
            message.add_alternative(body_html, subtype="html")

        # Handle attachment
        if attachment_path:
            if not os.path.exists(attachment_path):
                print(f" Attachment not found: {attachment_path}")
                return False

            mime_type, _ = mimetypes.guess_type(attachment_path)
            if mime_type is None:
                mime_type = "application/octet-stream"

            maintype, subtype = mime_type.split("/")

            try:
                with open(attachment_path, "rb") as file:
                    message.add_attachment(
                        file.read(),
                        maintype=maintype,
                        subtype=subtype,
                        filename=os.path.basename(attachment_path),
                    )
            except Exception as e:
                print(f" Failed to attach file: {e}")
                return False

        # Send message via SMTP
        try:
            with smtplib.SMTP(self.config.SMTP_SERVER, self.config.SMTP_PORT) as smtp:
                smtp.starttls()
                smtp.login(self.config.EMAIL, self.config.PASSWORD)
                smtp.send_message(message)

            print(f" Email successfully sent to {receiver}!")
            return True

        except Exception as error:
            print(f" Error sending email to {receiver}: {error}")
            return False

    def send_template_email(
        self,
        receiver: str,
        subject: str,
        template_name: str,
        context: Dict[str, Any],
        attachment_path: Optional[str] = None,
    ) -> bool:
        """Renders an HTML template and sends it to the recipient."""
        try:
            body_html, body_text = TemplateService.render(template_name, context)
            return self.send_email(
                receiver=receiver,
                subject=subject,
                body_text=body_text,
                body_html=body_html,
                attachment_path=attachment_path,
            )
        except Exception as e:
            print(f" Failed to render template '{template_name}': {e}")
            return False

    def send_bulk(
        self,
        receivers: List[str],
        subject: str,
        template_name: str,
        base_context: Dict[str, Any],
        delay_seconds: float = 0.2,
    ) -> Dict[str, bool]:
        """Sends template emails to multiple recipients using a single persistent SMTP connection for high performance."""
        import time

        valid, msg = self.config.validate()
        if not valid:
            print(f" Configuration error: {msg}")
            return {r: False for r in receivers}

        results = {}
        print(f"🚀 Initiating bulk email batch to {len(receivers)} recipient(s)...")

        try:
            # Re-use a single TCP/TLS connection for the entire batch
            with smtplib.SMTP(self.config.SMTP_SERVER, self.config.SMTP_PORT) as smtp:
                smtp.starttls()
                smtp.login(self.config.EMAIL, self.config.PASSWORD)

                for idx, receiver in enumerate(receivers, 1):
                    try:
                        context = base_context.copy()
                        context["email"] = receiver
                        if "name" not in context or context["name"] == "{{name}}":
                            context["name"] = receiver.split("@")[0].title()

                        body_html, body_text = TemplateService.render(template_name, context)

                        message = EmailMessage()
                        if self.config.FROM_NAME:
                            message["From"] = formataddr((self.config.FROM_NAME, self.config.EMAIL))
                        else:
                            message["From"] = self.config.EMAIL

                        message["To"] = receiver
                        message["Subject"] = subject
                        message.set_content(body_text)
                        message.add_alternative(body_html, subtype="html")

                        smtp.send_message(message)
                        print(f"  [{idx}/{len(receivers)}] Sent to {receiver}")
                        results[receiver] = True

                        if delay_seconds > 0:
                            time.sleep(delay_seconds)

                    except Exception as err:
                        print(f"  [{idx}/{len(receivers)}] Failed to send to {receiver}: {err}")
                        results[receiver] = False

        except Exception as batch_err:
            print(f" Bulk sending batch failed: {batch_err}")

        return results
