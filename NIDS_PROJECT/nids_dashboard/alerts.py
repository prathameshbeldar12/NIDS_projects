# nids_dashboard/alerts.py

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


# ================= OTP EMAIL =================
def send_otp_email(user, otp):
    """
    Send OTP email for password reset
    """

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
def send_attack_alert(user, detection):
    """
    Send attack alert email to user
    """

    if not user.email:
        return False

    message = f"""
🚨 ALERT: Attack Detected in NIDS System

Hello {user.username},

An attack has been detected.

Attack Type : {detection.attack_type}
Severity    : {detection.severity}
Confidence  : {detection.confidence}
Detected At : {detection.created_at}

Please log into dashboard immediately.

— NIDS Monitoring System
    """

    send_mail(
        subject="🚨 NIDS Alert – Attack Detected",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

    return True