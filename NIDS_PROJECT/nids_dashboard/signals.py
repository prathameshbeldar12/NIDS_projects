from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import DetectionResult
from .alerts import send_attack_alert


@receiver(post_save, sender=DetectionResult)
def send_attack_email_on_detection(sender, instance, created, **kwargs):

    if created:
        print("🔥 SIGNAL TRIGGERED")

        users = User.objects.exclude(email="")

        for user in users:
            print("Sending email to:", user.email)
            send_attack_alert(user, instance)