from django.shortcuts import render, redirect
from .models import OTPVerification
from loginsystem.models import Student, Company, Admin

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        email = request.session.get('pending_email')
        user_type = request.session.get('user_type')

        otp_obj = OTPVerification.objects.filter(email=email, user_type=user_type, otp=entered_otp).first()

        if otp_obj:
            # Set verified flag
            if user_type == 'student':
                Student.objects.filter(email=email).update(verified=True)
                return redirect('student')
            elif user_type == 'company':
                Company.objects.filter(company_email=email).update(verified=True)
                return redirect('company')
            elif user_type == 'admin':
                Admin.objects.filter(admin_email=email).update(verified=True)
                return redirect('admin')
        else:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})

    return render(request, 'verify_otp.html')
