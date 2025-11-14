from django.db import models

class OTPVerification(models.Model):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('company', 'Company'),
        ('admin', 'Admin'),
    )

    email = models.EmailField(default='default@email.com', unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} ({self.user_type}) - OTP: {self.otp}"
