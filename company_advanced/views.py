from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from loginsystem.models import Company
from .models import CompanyJob, Application, CompanyProfile

def company_advanced_dashboard(request):
    if not request.session.get('logged_in') or request.session.get('user_type') != 'company':
        messages.error(request, 'Please login as company first.')
        return redirect('login')
    
    company = Company.objects.get(company_email=request.session['email'])
    profile, created = CompanyProfile.objects.get_or_create(company=company)
    jobs = CompanyJob.objects.filter(company=company)
    total_applications = Application.objects.filter(job__company=company).count()
    
    context = {
        'company': company,
        'profile': profile,
        'jobs': jobs,
        'total_applications': total_applications,
        'active_jobs': jobs.filter(is_active=True),
    }
    return render(request, 'company_advanced/dashboard.html', context)

def post_jobs(request):
    if not request.session.get('logged_in') or request.session.get('user_type') != 'company':
        return redirect('login')
    
    company = Company.objects.get(company_email=request.session['email'])
    
    if request.method == 'POST':
        job = CompanyJob(
            company=company,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            requirements=request.POST.get('requirements'),
            job_type=request.POST.get('job_type', 'full_time'),
            location=request.POST.get('location'),
            salary=request.POST.get('salary'),
            deadline=request.POST.get('deadline'),
            vacancies=request.POST.get('vacancies', 1)
        )
        job.save()
        messages.success(request, 'Job posted successfully!')
        return redirect('post_jobs')
    
    jobs = CompanyJob.objects.filter(company=company)
    context = {
        'company': company,
        'jobs': jobs,
    }
    return render(request, 'company_advanced/post_jobs.html', context)

def view_applicants(request):
    if not request.session.get('logged_in') or request.session.get('user_type') != 'company':
        return redirect('login')
    
    company = Company.objects.get(company_email=request.session['email'])
    applications = Application.objects.filter(job__company=company).select_related('student', 'job')
    
    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    job_filter = request.GET.get('job', '')
    if job_filter:
        applications = applications.filter(job_id=job_filter)
    
    jobs = CompanyJob.objects.filter(company=company)
    
    context = {
        'company': company,
        'applications': applications,
        'jobs': jobs,
        'status_filter': status_filter,
        'job_filter': job_filter,
    }
    return render(request, 'company_advanced/applicants.html', context)

def update_application_status(request, application_id):
    if not request.session.get('logged_in') or request.session.get('user_type') != 'company':
        return redirect('login')
    
    application = get_object_or_404(Application, id=application_id)
    company = Company.objects.get(company_email=request.session['email'])
    
    if application.job.company != company:
        messages.error(request, 'Unauthorized action.')
        return redirect('view_applicants')
    
    new_status = request.POST.get('status')
    if new_status:
        application.status = new_status
        application.company_notes = request.POST.get('notes', '')
        application.save()
        messages.success(request, f'Application status updated to {new_status}')
    
    return redirect('view_applicants')
def company_profile(request):
    if not request.session.get('logged_in') or request.session.get('user_type') != 'company':
        return redirect('login')
    
    company = Company.objects.get(company_email=request.session['email'])
    profile, created = CompanyProfile.objects.get_or_create(company=company)
    
    # Get company statistics
    from .models import CompanyJob, Application
    total_jobs = CompanyJob.objects.filter(company=company).count()
    active_jobs = CompanyJob.objects.filter(company=company, is_active=True).count()
    total_applications = Application.objects.filter(job__company=company).count()
    
    if request.method == 'POST':
        # Update basic company info from registration
        company.company_name = request.POST.get('company_name', company.company_name)
        company.company_website = request.POST.get('company_website', company.company_website)
        company.industry = request.POST.get('industry', company.industry)
        company.company_address = request.POST.get('company_address', company.company_address)
        company.contact_name = request.POST.get('contact_name', company.contact_name)
        company.company_phone = request.POST.get('company_phone', company.company_phone)
        company.location = request.POST.get('location', company.location)
        company.job_profiles = request.POST.get('job_profiles', company.job_profiles)
        company.eligibility = request.POST.get('eligibility', company.eligibility)
        company.selection_process = request.POST.get('selection_process', company.selection_process)
        company.ctc = request.POST.get('ctc', company.ctc)
        company.internship = request.POST.get('internship', company.internship)
        company.other_info = request.POST.get('other_info', company.other_info)
        company.save()
        
        # Update advanced profile info
        profile.description = request.POST.get('description', '')
        profile.founded_year = request.POST.get('founded_year', '')
        profile.company_size = request.POST.get('company_size', '')
        profile.website = request.POST.get('website', '')
        profile.social_links = request.POST.get('social_links', '')
        profile.save()
        
        messages.success(request, 'Company profile updated successfully!')
        return redirect('company_profile')
    
    context = {
        'company': company,
        'profile': profile,
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'total_applications': total_applications,
    }
    return render(request, 'company_advanced/profile.html', context)