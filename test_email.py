import yagmail
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

receiver = EMAIL_USER  # Send to yourself

try:
    yag = yagmail.SMTP(user=EMAIL_USER, password=EMAIL_PASS)
    yag.send(
        to=receiver,
        subject="Test Email from Payslip Generator",
        contents="✅ This is a test email. If you received it, your email setup works!"
    )
    print("✅ Test email sent successfully.")
except Exception as e:
    print(f"❌ Failed to send test email: {e}")
