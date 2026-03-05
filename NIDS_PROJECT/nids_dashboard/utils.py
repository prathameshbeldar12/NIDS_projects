from django.core.mail import send_mail
from django.conf import settings


def send_attack_alert(user, message):
    print("🔥 send_attack_alert CALLED")
    print("Sending email to:", user.email)

    send_mail(
        subject="🚨 NIDS Alert – Attack Detected",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
