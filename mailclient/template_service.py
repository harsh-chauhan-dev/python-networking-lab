import os
import re
from typing import Dict, Any, Tuple

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")


class TemplateService:
    """Service for loading and rendering HTML templates with plain-text fallback."""

    @staticmethod
    def list_templates() -> list[str]:
        """Returns a list of available HTML template names."""
        if not os.path.exists(TEMPLATES_DIR):
            return []
        return [f for f in os.listdir(TEMPLATES_DIR) if f.endswith(".html")]

    @classmethod
    def load_template(cls, template_name: str) -> str:
        """Loads raw template content from file."""
        if not template_name.endswith(".html"):
            template_name += ".html"
        
        file_path = os.path.join(TEMPLATES_DIR, template_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Template '{template_name}' not found at {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    @classmethod
    def render(cls, template_name: str, context: Dict[str, Any]) -> Tuple[str, str]:
        """Renders an HTML template with context parameters and generates plain-text fallback.
        
        Returns:
            Tuple[html_content, plain_text_content]
        """
        raw_html = cls.load_template(template_name)

        # Replace {{key}} with values from context
        rendered_html = raw_html
        for key, value in context.items():
            pattern = r"\{\{\s*" + re.escape(str(key)) + r"\s*\}\}"
            rendered_html = re.sub(pattern, str(value), rendered_html)

        # Remove remaining unpopulated {{ placeholders }}
        rendered_html = re.sub(r"\{\{\s*[\w_]+\s*\}\}", "", rendered_html)

        # Create plain-text fallback from HTML
        plain_text = cls._html_to_plain_text(rendered_html)

        return rendered_html, plain_text

    @staticmethod
    def _html_to_plain_text(html: str) -> str:
        """Helper to convert HTML content into clean readable plain text."""
        # Replace <br> and <p> tags with newlines
        text = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
        text = re.sub(r"</p>", "\n\n", text, flags=re.IGNORECASE)
        text = re.sub(r"</div>", "\n", text, flags=re.IGNORECASE)
        text = re.sub(r"<h[1-6]>", "\n\n--- ", text, flags=re.IGNORECASE)
        text = re.sub(r"</h[1-6]>", " ---\n", text, flags=re.IGNORECASE)
        
        # Remove remaining HTML tags
        text = re.sub(r"<[^>]+>", "", text)
        
        # Collapse multiple blank lines
        text = re.sub(r"\n\s*\n", "\n\n", text)
        return text.strip()
