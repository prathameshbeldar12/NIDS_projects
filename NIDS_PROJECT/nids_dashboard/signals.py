from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import DetectionResult
from .alerts import send_attack_alert_bulk


@receiver(post_save, sender=DetectionResult)
def send_attack_email_on_detection(sender, instance, created, **kwargs):

    if not created:
        return

    # Ignore normal traffic
    if instance.attack_type.lower() == "normal":
        return

    print("🚨 Attack detected, preparing email")

    # Get last 10 attack records (not normal)
    detections = DetectionResult.objects.exclude(
        attack_type__iexact="normal"
    ).order_by("-created_at")[:10]

    users = User.objects.exclude(email="")

    for user in users:
        print("Sending alert to:", user.email)
        send_attack_alert_bulk(user, detections)