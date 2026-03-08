# nids_dashboard/alerts.py

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


# ================= OTP EMAIL =================
def send_otp_email(user, otp):

    if not user.email:
        return False

    message = f"""
Hello {user.username},

🔐 Your NIDS Password Reset OTP is:

{otp}

⏳ This OTP is valid for 5 minutes.

If you did not request this, please ignore this email.

— NIDS Security Team
Time: {timezone.now()}
"""

    send_mail(
        subject="🔐 NIDS Password Reset OTP",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

    return True


# ================= ATTACK ALERT EMAIL =================
def send_attack_alert_bulk(user, detections):

    if not user.email:
        return False

    attack_logs = ""

    for d in detections:
        attack_logs += f"""
Attack Type : {d.attack_type}
Severity    : {d.severity}
Confidence  : {d.confidence}
Detected At : {d.created_at}
-----------------------------------------
"""

    message = f"""
🚨 NIDS SECURITY ALERT 🚨

Hello {user.username},

The following attacks were detected in the system:

{attack_logs}

Please login to the dashboard for full details.

— NIDS Monitoring System
"""

    send_mail(
        subject="🚨 Multiple Attacks Detected - NIDS",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

    return True