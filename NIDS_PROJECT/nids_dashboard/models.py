from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# ================= FILE UPLOAD =================

class UploadedFile(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="uploaded_files"
    )
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"


# ================= DETECTION RESULT =================

class DetectionResult(models.Model):

    SEVERITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="detections"
    )

    attack_type = models.CharField(max_length=100)
    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default="Low"
    )
    confidence = models.FloatField(default=0.0)

    raw_data = models.TextField(
        blank=True,
        null=True,
        help_text="Original CSV row data"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["attack_type"]),
            models.Index(fields=["severity"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.attack_type} | {self.severity} | {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


# ================= USER ALERT SETTINGS =================

class UserAlertSetting(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="alert_settings"
    )

    phone_number = models.CharField(max_length=15, blank=True)
    email_alert = models.BooleanField(default=True)
    sms_alert = models.BooleanField(default=False)

    def __str__(self):
        return f"Alert Settings - {self.user.username}"


# ================= PASSWORD RESET OTP =================

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="password_otps"
    )
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - OTP"
