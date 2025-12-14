"""
Simple test script to verify SMTP email configuration.
Run this to test your Gmail SMTP setup before using the API.
"""

import os
from dotenv import load_dotenv
from email_utils import send_email_with_attachment
from pathlib import Path

# Load environment variables
load_dotenv()

def test_basic_email():
    """Test sending a basic email without attachment."""
    print("🔍 Testing SMTP configuration...\n")
    
    # Check environment variables
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    
    print(f"📧 SMTP Email: {smtp_email}")
    print(f"🔑 Password: {'*' * len(smtp_password) if smtp_password else 'NOT SET'}")
    print(f"🌐 Host: {smtp_host}")
    print(f"🔌 Port: {smtp_port}\n")
    
    if not smtp_email or not smtp_password:
        print("❌ Error: SMTP_EMAIL and SMTP_PASSWORD must be set in .env file")
        return False
    
    # Ask for test recipient
    recipient = input(f"Enter recipient email (press Enter to send to yourself at {smtp_email}): ").strip()
    if not recipient:
        recipient = smtp_email
    
    print(f"\n📤 Sending test email to {recipient}...")
    
    try:
        # Create a simple test PDF if one doesn't exist
        test_pdf = Path("test_email_attachment.pdf")
        if not test_pdf.exists():
            # Create a minimal PDF
            with open(test_pdf, "wb") as f:
                f.write(b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> >> >> /MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 44 >>\nstream\nBT /F1 12 Tf 100 700 Td (Test Email Attachment) Tj ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000058 00000 n\n0000000115 00000 n\n0000000317 00000 n\ntrailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n410\n%%EOF")
            print(f"✓ Created test PDF: {test_pdf}")
        
        send_email_with_attachment(
            smtp_user=smtp_email,
            smtp_password=smtp_password,
            to_email=recipient,
            subject="Test Email - LoanAI SMTP Configuration",
            body="This is a test email from your LoanAI application.\n\nIf you received this, your SMTP configuration is working correctly!",
            attachment_path=str(test_pdf),
            smtp_host=smtp_host,
            smtp_port=smtp_port,
        )
        
        print(f"✅ Email sent successfully to {recipient}!")
        print(f"📬 Check your inbox (and spam folder) to confirm delivery.")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        print("\n💡 Common issues:")
        print("   - If using Gmail with 2FA, you MUST use an App Password, not your regular password")
        print("   - Get App Password at: https://myaccount.google.com/apppasswords")
        print("   - Check if 'Less secure app access' is enabled (if not using 2FA)")
        print("   - Verify your email and password are correct in .env file")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("  LoanAI SMTP Configuration Test")
    print("=" * 60)
    print()
    
    success = test_basic_email()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ SMTP configuration is working!")
        print("\nYou can now use the API endpoint:")
        print("POST /api/send-sanction-letter/{session_id}?user_id={user_id}")
    else:
        print("❌ SMTP configuration needs fixing")
        print("\nPlease check your .env file and try again")
    print("=" * 60)
