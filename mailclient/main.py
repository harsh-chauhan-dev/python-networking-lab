import os
import sys
from datetime import datetime
from smtp_service import EmailService
from template_service import TemplateService
from config import Config


def print_banner():
    print("\n" + "=" * 45)
    print("      📧 PYTHON MAIL CLIENT SERVICES      ")
    print("=" * 45)


def handle_send_plain(service: EmailService):
    print("\n--- Send Plain Text Email ---")
    receiver = input("Receiver Email: ").strip()
    subject = input("Subject: ").strip()
    body = input("Message Content: ").strip()
    attach = input("Attachment path (leave blank for none): ").strip() or None

    service.send_email(
        receiver=receiver,
        subject=subject,
        body_text=body,
        attachment_path=attach,
    )


def handle_send_template(service: EmailService):
    print("\n--- Send HTML Template Email ---")
    templates = TemplateService.list_templates()
    if not templates:
        print("❌ No HTML templates available.")
        return

    print("Available HTML Templates:")
    for idx, t_name in enumerate(templates, 1):
        print(f"  {idx}. {t_name}")

    t_choice = input(f"Choose template (1-{len(templates)}): ").strip()
    try:
        template_name = templates[int(t_choice) - 1]
    except (ValueError, IndexError):
        print("❌ Invalid template choice.")
        return

    receiver = input("Receiver Email: ").strip()
    subject = input("Subject: ").strip()

    # Build context dynamic parameters based on selected template
    context = {
        "year": datetime.now().year,
        "date": datetime.now().strftime("%B %d, %Y"),
        "sender_name": "Python Networking Lab",
        "company": "Python NetLab Inc.",
    }

    if "welcome" in template_name:
        context["name"] = input("Recipient Name (default: Friend): ").strip() or "Friend"
        context["message"] = input("Welcome Message: ").strip() or "We are excited to have you on board with Python Mail Client Services!"
        context["action_url"] = input("Action URL (e.g. https://example.com): ").strip() or "https://github.com"

    elif "notification" in template_name:
        context["name"] = input("Recipient Name: ").strip() or "User"
        context["status"] = input("Status (INFO/SUCCESS/WARNING): ").strip() or "SUCCESS"
        context["title"] = input("Notification Title: ").strip() or "System Activity Detected"
        context["details"] = input("Details Message: ").strip() or "Your request has been processed successfully."
        context["event_name"] = input("Event Name: ").strip() or "User Login / Action"
        context["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        context["priority"] = "Normal"

    elif "newsletter" in template_name:
        context["subscriber_name"] = input("Subscriber Name: ").strip() or "Subscriber"
        context["newsletter_title"] = input("Newsletter Title: ").strip() or "Tech & Networking Digest"
        context["issue_number"] = "42"
        context["headline_1"] = input("Headline 1: ").strip() or "Python Mail Client Modular Services Released"
        context["content_1"] = input("Content 1: ").strip() or "Our email client now supports modular SMTP, Template rendering, and HTML email templates."
        context["headline_2"] = input("Headline 2: ").strip() or "Upcoming Features"
        context["content_2"] = input("Content 2: ").strip() or "Stay tuned for IMAP receiving and REST API integration."

    attach = input("Attachment path (leave blank for none): ").strip() or None

    service.send_template_email(
        receiver=receiver,
        subject=subject,
        template_name=template_name,
        context=context,
        attachment_path=attach,
    )


def handle_send_custom_html(service: EmailService):
    print("\n--- Send Custom HTML Email ---")
    receiver = input("Receiver Email: ").strip()
    subject = input("Subject: ").strip()
    print("Enter HTML Body (type 'END' on a new line when done):")
    html_lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        html_lines.append(line)
    body_html = "\n".join(html_lines)
    body_text = TemplateService._html_to_plain_text(body_html)

    attach = input("Attachment path (leave blank for none): ").strip() or None

    service.send_email(
        receiver=receiver,
        subject=subject,
        body_text=body_text,
        body_html=body_html,
        attachment_path=attach,
    )


def handle_send_bulk(service: EmailService):
    print("\n--- Send Bulk Template Emails ---")
    recipients_raw = input("Enter Receiver Emails (comma separated): ").strip()
    receivers = list(dict.fromkeys(
        r.strip().lower()
        for r in recipients_raw.split(",")
        if r.strip()
    ))
    print(f"Total unique receivers: {len(receivers)}")

    if not receivers:
        print("❌ No valid receivers provided.")
        return

    subject = input("Subject: ").strip()
    template_name = "welcome.html"
    base_context = {
        "company": "Python NetLab Services",
        "sender_name": "Networking Admin",
        "message": "Welcome to our platform!",
        "action_url": "https://github.com",
        "year": datetime.now().year,
    }

    results = service.send_bulk(
        receivers=receivers,
        subject=subject,
        template_name=template_name,
        base_context=base_context,
    )

    print("\n📊 Bulk Sending Report:")
    for email, status in results.items():
        symbol = "✅ Sent" if status else "❌ Failed"
        print(f"  - {email}: {symbol}")


def handle_test_connection(service: EmailService):
    print("\n--- Testing SMTP Connection ---")
    success, msg = service.test_connection()
    if success:
        print(f"✅ {msg}")
    else:
        print(f"❌ {msg}")


def main():
    service = EmailService()

    while True:
        print_banner()
        print("1. Send Quick Plain Text Email")
        print("2. Send HTML Template Email (Welcome / Alert / Newsletter)")
        print("3. Send Custom HTML Email")
        print("4. Send Bulk Template Emails")
        print("5. Test SMTP Connection & Validate Settings")
        print("6. Exit")

        choice = input("\nSelect a service option (1-6): ").strip()

        if choice == "1":
            handle_send_plain(service)
        elif choice == "2":
            handle_send_template(service)
        elif choice == "3":
            handle_send_custom_html(service)
        elif choice == "4":
            handle_send_bulk(service)
        elif choice == "5":
            handle_test_connection(service)
        elif choice == "6":
            print("\n👋 Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid option. Please select 1-6.")


if __name__ == "__main__":
    main()