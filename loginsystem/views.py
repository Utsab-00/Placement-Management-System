from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student, Company, Admin
from django.middleware.csrf import get_token

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
                password=password
            )
            student.save()
            messages.success(request, "Student added successfully.")

        return redirect("student_list")

    students = Student.objects.all()
    return render(request, "students.html", {"students": students})


# Company List + Add Company
def company_list(request):
    if request.method == "POST":
        company_name = request.POST.get("company_name")
        website = request.POST.get("website")
        industry = request.POST.get("industry")
        address = request.POST.get("address")
        contact_name = request.POST.get("contact_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        job_profiles = request.POST.get("job_profiles")
        location = request.POST.get("location")
        eligibility = request.POST.get("eligibility")
        selection_process = request.POST.get("selection_process")
        ctc = request.POST.get("ctc")
        internship = request.POST.get("internship")
        other_info = request.POST.get("other_info")
        password = request.POST.get("password")

        if company_name and email and password:
            company = Company(
                company_name=company_name,
                website=website,
                industry=industry,
                address=address,
                contact_name=contact_name,
                email=email,
                phone=phone,
                job_profiles=job_profiles,
                location=location,
                eligibility=eligibility,
                selection_process=selection_process,
                ctc=ctc,
                internship=internship or "No",
                other_info=other_info,
                password=password
            )
            company.save()
            messages.success(request, "Company added successfully.")

        return redirect("company_list")

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
                password=password
            )
            admin.save()
            messages.success(request, "Admin added successfully.")

        return redirect("admin_list")

    admins = Admin.objects.all()
    return render(request, "admins.html", {"admins": admins})


# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        user = None

        if user_type == 'admin':
            user = Admin.objects.filter(admin_name=username).first()
        elif user_type == 'student':
            user = Student.objects.filter(name=username).first()
        elif user_type == 'company':
            user = Company.objects.filter(company_name=username).first()

        if user and user.check_password(password):
            request.session['logged_in'] = True
            request.session['username'] = username
            request.session['user_type'] = user_type
            request.session["csrf_token"] = get_token(request)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


# Logout View
def logout_view(request):
    request.session.flush()
    messages.success(request, 'You have been logged out.')
    return redirect('login')

# Dashboards
def admin_page(request):
    """Render the admin page."""
    return render(request, 'admin_page.html')

def company_page(request):
    """Render the company page."""
    return render(request, 'company_page.html')

def student_page(request):
    """Render the student page."""
    return render(request, 'student_page.html')