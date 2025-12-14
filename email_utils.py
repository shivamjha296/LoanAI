import os
import smtplib
from pathlib import Path
from email.message import EmailMessage
from typing import Optional


def send_email_with_attachment(
    smtp_user: str,
    smtp_password: str,
    to_email: str,
    subject: str,
    body: str,
    attachment_path: str,
    smtp_host: str = "smtp.gmail.com",
    smtp_port: int = 465,
):
    """Send an email with a single file attachment.

    Supports SSL (port 465) and STARTTLS (other ports like 587).
    Raises exceptions on failure.
    """
    if not smtp_user or not smtp_password:
        raise ValueError("SMTP credentials not provided")

    path = Path(attachment_path)
    if not path.exists():
        raise FileNotFoundError(f"Attachment not found: {attachment_path}")

    msg = EmailMessage()
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    # Attach file (assume PDF for sanction letter)
    with path.open("rb") as f:
        data = f.read()
    msg.add_attachment(data, maintype="application", subtype="pdf", filename=path.name)

    # Send
    if smtp_port == 465:
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
    else:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)


def send_sanction_letter_for_session(session_state: dict, smtp_user: Optional[str] = None, smtp_password: Optional[str] = None):
    """Helper that reads `sanction_letter` and `customer_email` from session state and sends the PDF.

    Reads SMTP settings from environment if `smtp_user`/`smtp_password` are not provided.
    """
    smtp_user = smtp_user or os.getenv("SMTP_EMAIL")
    smtp_password = smtp_password or os.getenv("SMTP_PASSWORD")
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))

    customer_email = session_state.get("customer_email") or session_state.get("customer_email_address")
    if not customer_email:
        # Try to fetch from customer info
        customer = session_state.get("customer_id")
        raise ValueError("Customer email not found in session state")

    sanction = session_state.get("sanction_letter", {})
    pdf_file = sanction.get("pdf_file_path")
    if not pdf_file:
        raise ValueError("No sanction letter PDF path found in session state")

    subject = f"Sanction Letter - {sanction.get('sanction_reference', '')}"
    body = (
        f"Dear {session_state.get('customer_name', '')},\n\n"
        "Please find attached your sanction letter for the loan application.\n\n"
        "Regards,\nTata Capital Loan Assistant"
    )

    send_email_with_attachment(
        smtp_user=smtp_user,
        smtp_password=smtp_password,
        to_email=customer_email,
        subject=subject,
        body=body,
        attachment_path=pdf_file,
        smtp_host=smtp_host,
        smtp_port=smtp_port,
    )
