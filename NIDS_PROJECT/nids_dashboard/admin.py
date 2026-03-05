from django.contrib import admin
from .models import (
    UploadedFile,
    DetectionResult,
    UserAlertSetting,
    PasswordResetOTP
)

admin.site.register(UploadedFile)
admin.site.register(DetectionResult)
admin.site.register(UserAlertSetting)
admin.site.register(PasswordResetOTP)
