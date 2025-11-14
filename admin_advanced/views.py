from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from loginsystem.models import Student, Company, Admin
from .models import PlacementReport, SystemAnalytic, Announcement, PlacementDrive, ContactMessage

def admin_advanced_dashboard(request):
    if not request.session.get('logged_in') or request.session.get('user_type') != 'admin':
        messages.error(request, 'Please login as admin first.')
        return redirect('login')
    
    admin_user = Admin.objects.get(admin_email=request.session['email'])
    
    total_students = Student.objects.count()
    total_companies = Company.objects.count()
    verified_students = Student.objects.filter(verified=True).count()
    verified_companies = Company.objects.filter(verified=True).count()
    
    recent_announcements = Announcement.objects.filter(is_active=True).order_by('-created_date')[:5]
    
    context = {
        'admin': admin_user,
        'total_students': total_students,
        'total_companies': total_companies,
        'verified_students': verified_students,
        'verified_companies': verified_companies,
        'recent_announcements': recent_announcements,
    }
    return render(request, 'admin_advanced/dashboard.html', context)

def manage_students(request):
    if not request.session.get('logged_in') or request.session.get('user_type') != 'admin':
        return redirect('login')
    
    students = Student.objects.all().order_by('-id')
    
    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(name__icontains=search_query) | students.filter(email__icontains=search_query)
    
    status_filter = request.GET.get('status', '')
    if status_filter == 'verified':
        students = students.filter(verified=True)
    elif status_filter == 'unverified':
        students = students.filter(verified=False)
    
    context = {
        'students': students,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'admin_advanced/manage_students.html', context)

def manage_companies(request):
    if not request.session.get('logged_in') or request.session.get('user_type') != 'admin':
        return redirect('login')
    
    companies = Company.objects.all().order_by('-id')
    
    search_query = request.GET.get('search', '')
    if search_query:
        companies = companies.filter(company_name__icontains=search_query) | companies.filter(company_email__icontains=search_query)
    
    status_filter = request.GET.get('status', '')
    if status_filter == 'verified':
        companies = companies.filter(verified=True)
    elif status_filter == 'unverified':
        companies = companies.filter(verified=False)
    
    context = {
        'companies': companies,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'admin_advanced/manage_company.html', context)

def manage_jobs(request):
    if not request.session.get('logged_in') or request.session.get('user_type') != 'admin':
        return redirect('login')
    
    from company_advanced.models import CompanyJob
    jobs = CompanyJob.objects.all().select_related('company').order_by('-posted_date')
    
    active_filter = request.GET.get('active', '')
    if active_filter == 'active':
        jobs = jobs.filter(is_active=True)
    elif active_filter == 'inactive':
        jobs = jobs.filter(is_active=False)
    
    context = {
        'jobs': jobs,
        'active_filter': active_filter,
    }
    return render(request, 'admin_advanced/manage_job.html', context)

def toggle_verification(request, user_type, user_id):
    if not request.session.get('logged_in') or request.session.get('user_type') != 'admin':
        return redirect('login')
    
    if user_type == 'student':
        user = get_object_or_404(Student, id=user_id)
    elif user_type == 'company':
        user = get_object_or_404(Company, id=user_id)
    else:
        messages.error(request, 'Invalid user type.')
        return redirect('admin_advanced_dashboard')
    
    user.verified = not user.verified
    user.save()
    
    status = "verified" if user.verified else "unverified"
    messages.success(request, f'{user.name if user_type == "student" else user.company_name} has been {status}.')
    
    if user_type == 'student':
        return redirect('manage_students')
    else:
        return redirect('manage_companies')
def admin_profile(request):
    if not request.session.get('logged_in') or request.session.get('user_type') != 'admin':
        messages.error(request, 'Please login as admin first.')
        return redirect('login')
    
    admin_user = Admin.objects.get(admin_email=request.session['email'])
    
    # Get system statistics
    from loginsystem.models import Student, Company
    total_students = Student.objects.count()
    total_companies = Company.objects.count()
    verified_students = Student.objects.filter(verified=True).count()
    verified_companies = Company.objects.filter(verified=True).count()
    
    if request.method == 'POST':
        # Update admin info from registration
        admin_user.admin_name = request.POST.get('admin_name', admin_user.admin_name)
        admin_user.admin_phone = request.POST.get('admin_phone', admin_user.admin_phone)
        admin_user.department = request.POST.get('department', admin_user.department)
        admin_user.role = request.POST.get('role', admin_user.role)
        admin_user.experience = request.POST.get('experience', admin_user.experience)
        admin_user.save()
        
        messages.success(request, 'Admin profile updated successfully!')
        return redirect('admin_profile')
    
    context = {
        'admin': admin_user,
        'total_students': total_students,
        'total_companies': total_companies,
        'verified_students': verified_students,
        'verified_companies': verified_companies,
    }
    return render(request, 'admin_advanced/profile.html', context)