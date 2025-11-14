from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student, Company, Admin
from django.middleware.csrf import get_token
from emailverification.utils import send_otp_email

# Home page
def home(request):
    return render(request, 'home.html')

# Student List + Add Student
def student_list(request):
    if request.method == "POST":
        name = request.POST.get("name")
        student_id = request.POST.get("student_id")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        branch = request.POST.get("branch")
        year_of_study = request.POST.get("year_of_study")
        cgpa = request.POST.get("cgpa")
        skills = request.POST.get("skills")
        resume_link = request.POST.get("resume_link")
        password = request.POST.get("password")

        if name and student_id and password:
            student = Student(
                name=name,
                student_id=student_id,
                email=email,
                phone_number=phone_number,
                branch=branch,
                year_of_study=year_of_study,
                cgpa=cgpa if cgpa else None,
                skills=skills,
                resume_link=resume_link,
                password=password,
                verified=False
            )
            student.save()

            # AUTO-CREATE STUDENT PROFILE
            from student_advanced.models import StudentProfile
            StudentProfile.objects.create(student=student)
            
            send_otp_email(email, 'student')
            request.session['pending_email'] = email
            request.session['user_type'] = 'student'
            return redirect('emailverification:verify_otp')

    students = Student.objects.all()
    return render(request, "students.html", {"students": students})

# Company List + Add Company
def company_list(request):
    if request.method == "POST":
        company_name = request.POST.get("company_name")
        company_website = request.POST.get("company_website")
        industry = request.POST.get("industry")
        company_address = request.POST.get("company_address")
        contact_name = request.POST.get("contact_name")
        company_email = request.POST.get("company_email")
        company_phone = request.POST.get("company_phone")
        job_profiles = request.POST.get("job_profiles")
        location = request.POST.get("location")
        eligibility = request.POST.get("eligibility")
        selection_process = request.POST.get("selection_process")
        ctc = request.POST.get("ctc")
        internship = request.POST.get("internship")
        other_info = request.POST.get("other_info")
        password = request.POST.get("password")

        if company_name and company_email and password:
            company = Company(
                company_name=company_name,
                company_website=company_website,
                industry=industry,
                company_address=company_address,
                contact_name=contact_name,
                company_email=company_email,
                company_phone=company_phone,
                job_profiles=job_profiles,
                location=location,
                eligibility=eligibility,
                selection_process=selection_process,
                ctc=ctc,
                internship=internship or "No",
                other_info=other_info,
                password=password,
                verified=False
            )
            company.save()

            # AUTO-CREATE COMPANY PROFILE
            from company_advanced.models import CompanyProfile
            CompanyProfile.objects.create(company=company)
            
            send_otp_email(company_email, 'company')
            request.session['pending_email'] = company_email
            request.session['user_type'] = 'company'
            return redirect('emailverification:verify_otp')

    companies = Company.objects.all()
    return render(request, "companies.html", {"companies": companies})

# Admin List + Add Admin
def admin_list(request):
    if request.method == "POST":
        admin_name = request.POST.get("admin_name")
        admin_id = request.POST.get("admin_id")
        admin_email = request.POST.get("admin_email")
        admin_phone = request.POST.get("admin_phone")
        department = request.POST.get("department")
        role = request.POST.get("role")
        experience = request.POST.get("experience")
        password = request.POST.get("password")

        if admin_name and admin_id and admin_email and password:
            admin = Admin(
                admin_name=admin_name,
                admin_id=admin_id,
                admin_email=admin_email,
                admin_phone=admin_phone,
                department=department,
                role=role,
                experience=int(experience) if experience else None,
                password=password,
                verified=False
            )
            admin.save()

            send_otp_email(admin_email, 'admin')
            request.session['pending_email'] = admin_email
            request.session['user_type'] = 'admin'
            return redirect('emailverification:verify_otp')

    admins = Admin.objects.all()
    return render(request, "admins.html", {"admins": admins})

# Login View
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        user = None

        if user_type == 'admin':
            user = Admin.objects.filter(admin_email=email).first()
        elif user_type == 'student':
            user = Student.objects.filter(email=email).first()
        elif user_type == 'company':
            user = Company.objects.filter(company_email=email).first()

        # Use the model's check_password method
        if user and user.check_password(password):
            if not user.verified:
                messages.error(request, 'Please verify your email first.')
                return redirect('login')

            request.session['logged_in'] = True
            request.session['email'] = email
            request.session['user_type'] = user_type
            request.session['user_id'] = user.id
            request.session["csrf_token"] = get_token(request)
            
            # Redirect to BASIC dashboard first
            if user_type == 'student':
                return redirect('student')
            elif user_type == 'company':
                return redirect('company')
            elif user_type == 'admin':
                return redirect('admin')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')

# Logout View
def logout_view(request):
    request.session.flush()
    messages.success(request, 'You have been logged out.')
    return redirect('login')

# UPDATED BASIC DASHBOARDS
def student_page(request):
    if not request.session.get('logged_in') or request.session.get('user_type') != 'student':
        return redirect('login')
    
    student = Student.objects.get(email=request.session['email'])
    
    # LAZY IMPORT to avoid circular imports
    from student_advanced.models import JobApplication
    total_applications = JobApplication.objects.filter(student=student).count()
    interviews_scheduled = JobApplication.objects.filter(student=student, status='interview').count()
    
    context = {
        'student': student,
        'total_applications': total_applications,
        'interviews_scheduled': interviews_scheduled,
    }
    return render(request, 'student_page.html', context)

def company_page(request):
    if not request.session.get('logged_in') or request.session.get('user_type') != 'company':
        return redirect('login')
    
    company = Company.objects.get(company_email=request.session['email'])
    
    # LAZY IMPORT to avoid circular imports
    from company_advanced.models import CompanyJob, Application
    total_jobs = CompanyJob.objects.filter(company=company).count()
    total_applications = Application.objects.filter(job__company=company).count()
    
    context = {
        'company': company,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
    }
    return render(request, 'company_page.html', context)

def admin_page(request):
    if not request.session.get('logged_in') or request.session.get('user_type') != 'admin':
        return redirect('login')
    
    admin = Admin.objects.get(admin_email=request.session['email'])
    
    # Get some basic stats for the basic dashboard
    total_students = Student.objects.count()
    total_companies = Company.objects.count()
    verified_students = Student.objects.filter(verified=True).count()
    verified_companies = Company.objects.filter(verified=True).count()
    
    context = {
        'admin': admin,
        'total_students': total_students,
        'total_companies': total_companies,
        'verified_students': verified_students,
        'verified_companies': verified_companies,
    }
    return render(request, 'admin_page.html', context)

# NEW VIEW: Redirect to Advanced Dashboard
def redirect_to_advanced_dashboard(request):
    if not request.session.get('logged_in'):
        messages.error(request, 'Please login first.')
        return redirect('login')
    
    user_type = request.session.get('user_type')
    
    if user_type == 'student':
        return redirect('student_advanced_dashboard')  # Make sure this matches
    elif user_type == 'company':
        return redirect('company_advanced_dashboard')  # Make sure this matches
    elif user_type == 'admin':
        return redirect('admin_advanced_dashboard')    # Make sure this matches
    else:
        messages.error(request, 'Invalid user type.')
        return redirect('home')