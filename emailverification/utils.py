import random
from django.core.mail import send_mail
from .models import OTPVerification

def generate_otp(length=6):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def send_otp_email(email, user_type):
    otp = generate_otp()
    OTPVerification.objects.update_or_create(
        email=email,
        user_type=user_type,
        defaults={'otp': otp}
    )

    send_mail(
        subject="Your OTP Code",
        message=f"Your OTP is: {otp}",
        from_email="youremail@example.com",  # Replace this
        recipient_list=[email],
    )
