import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SENDER = os.getenv("EMAIL_SENDER")
PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER = os.getenv("EMAIL_SENDER")  # sending to yourself


def send_alert(subject, body):
    """Send an email alert when data quality fails."""
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER
        msg["To"] = RECEIVER
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, RECEIVER, msg.as_string())
        server.quit()

        print(f"✅ Alert sent: {subject}")

    except Exception as e:
        print(f"❌ Failed to send alert: {e}")


def check_and_alert(quality_results):
    """
    Reads quality check results and sends alert if anything failed.
    quality_results is a dict like:
    {
        'row_count': {'passed': True, 'value': 1000},
        'null_check': {'passed': False, 'value': 0.15},
        'duplicate_check': {'passed': True, 'value': 0.0}
    }
    """
    failed_checks = []

    for check_name, result in quality_results.items():
        if not result["passed"]:
            failed_checks.append(f"  ❌ {check_name}: {result['value']}")

    if failed_checks:
        subject = f"🚨 PulseCheck Alert — Data Quality Failed {datetime.now().strftime('%Y-%m-%d')}"
        body = f"""
PulseCheck Data Quality Alert
==============================
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

The following checks FAILED:

{chr(10).join(failed_checks)}

Please investigate the pipeline immediately.

— PulseCheck Monitoring System
        """
        send_alert(subject, body)
    else:
        print("✅ All quality checks passed — no alert needed.")


# --- Test it directly ---
if __name__ == "__main__":
    test_results = {
        "row_count": {"passed": True, "value": 1000},
        "null_check": {"passed": False, "value": 0.15},
        "duplicate_check": {"passed": True, "value": 0.0}
    }
    check_and_alert(test_results)