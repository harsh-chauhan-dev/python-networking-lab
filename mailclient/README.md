# 📧 Python Mail Client & Email Services

A modular, full-featured Python email client and service laboratory built using standard library `smtplib`, `email.message`, and custom HTML template rendering.

This project is part of the **Python Networking Lab** series to help you understand email networking protocols (SMTP/TLS), MIME multi-part message construction, and modular service design in Python.

---

## 🎯 What You Are Supposed to Learn & Do in This Project

In this project, you will understand how email communication works at the application layer:
1. **SMTP & TLS Encryption**: Handshake, STARTTLS security, and SMTP authentication with email providers (e.g., Gmail, Outlook).
2. **MIME Message Construction**: Building multi-part emails containing both plain text and HTML bodies with fallbacks and file attachments.
3. **Template Engine & Variable Substitution**: Dynamic placeholder replacement (`{{name}}`, `{{message}}`) for transactional and marketing emails.
4. **Modular Architecture**: Separating configuration, template parsing, network transport, and user interface.

---

## 📁 Project Structure

```
mailclient/
├── .env                  # Environment variables (Credentials & SMTP settings)
├── config.py             # Configuration loader & credential validation service
├── template_service.py   # Template loader, placeholder renderer & plain-text fallback generator
├── smtp_service.py       # EmailService (SMTP TLS, MIME message builder, bulk sending)
├── main.py               # Interactive CLI Service Hub
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation & lab guide
└── templates/            # HTML Email Templates
    ├── welcome.html      # Welcome email template with CTA button
    ├── notification.html # System alert & status table template
    └── newsletter.html   # Structured newsletter template
```

---

## 🛠️ Prerequisites & Setup

### 1. Configure Gmail / SMTP Credentials

To send emails using Gmail SMTP, you need an **App Password** (not your regular Gmail password):
1. Enable **2-Step Verification** on your Google Account.
2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords).
3. Generate a new App Password for "Mail".
4. Copy the 16-character password into your `.env` file.

### 2. Configure `.env` File

Ensure `.env` in the `mailclient/` directory has your credentials:

```env
EMAIL=your-email@gmail.com
PASSWORD=your-16-char-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### 3. Install Dependencies

```bash
cd mailclient
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

---

## 🚀 How to Run the Project

Run the main CLI service hub:

```bash
python main.py
```

### Interactive Menu Options:

1. **Send Quick Plain Text Email**: Send a simple text message with an optional attachment.
2. **Send HTML Template Email**: Select a template (`welcome.html`, `notification.html`, or `newsletter.html`), fill in dynamic values, and send a rich HTML email.
3. **Send Custom HTML Email**: Paste custom raw HTML code directly in the terminal to send.
4. **Send Bulk Template Emails**: Send template-rendered emails to multiple recipient addresses.
5. **Test SMTP Connection**: Verify if your credentials and SMTP connection work without sending an email.

---

## 🧪 Hands-On Lab Exercises for You to Complete

To deepen your networking & Python skills, try implementing these tasks:

### Task 1: Create a Custom HTML Template
- Create a new file `templates/password_reset.html`.
- Add a reset password button and placeholders for `{{username}}` and `{{reset_link}}`.
- Test sending it via Option 2 in `main.py`.

### Task 2: Add IMAP Email Receiving Support (Challenge)
- Create `imap_service.py` using Python's built-in `imaplib` module.
- Add a service method to connect to `imap.gmail.com:993` (SSL) and fetch unread email subjects.

### Task 3: File Logging
- Modify `config.py` and `smtp_service.py` to log all email activity (sent status, errors, timestamps) into a `mailclient.log` file using Python's `logging` module.
