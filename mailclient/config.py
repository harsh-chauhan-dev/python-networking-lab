import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    EMAIL = os.getenv("EMAIL", "").strip()
    PASSWORD = os.getenv("PASSWORD", "").strip()
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com").strip()
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    FROM_NAME = os.getenv("FROM_NAME", "MailClient").strip()

    @classmethod
    def validate(cls) -> tuple[bool, str]:
        """Validates that essential SMTP configuration is provided."""
        if not cls.EMAIL:
            return False, "EMAIL is missing in environment variables (.env)."
        if not cls.PASSWORD:
            return False, "PASSWORD is missing in environment variables (.env)."
        if not cls.SMTP_SERVER:
            return False, "SMTP_SERVER is missing in environment variables (.env)."
        return True, "Configuration is valid."
