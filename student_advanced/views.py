from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from loginsystem.models import Student
from .models import Job, JobApplication, StudentProfile, Interview

def student_advanced_dashboard(request):
    if not request.session.get('logged_in') or request.session.get('user_type') != 'student':
        messages.error(request, 'Please login as student first.')
        return redirect('login')
    
    student = Student.objects.get(email=request.session['email'])
    profile, created = StudentProfile.objects.get_or_create(student=student)
    applications = JobApplication.objects.filter(student=student)
    interviews = Interview.objects.filter(application__student=student)
    
    context = {
        'student': student,
        'profile': profile,
        'applications': applications,
        'interviews': interviews,
        'total_applications': applications.count(),
        'upcoming_interviews': interviews.filter(interview_date__gte=timezone.now()),
    }
    return render(request, 'student_advanced/dashboard.html', context)

def student_jobs(request):
    if not request.session.get('logged_in') or request.session.get('user_type') != 'student':
        return redirect('login')
    
    jobs = Job.objects.filter(is_active=True, deadline__gte=timezone.now().date())
    student = Student.objects.get(email=request.session['email'])
    
    applied_jobs = JobApplication.objects.filter(student=student).values_list('job_id', flat=True)
    
    context = {
        'jobs': jobs,
        'applied_jobs': applied_jobs,
    }
    return render(request, 'student_advanced/jobs.html', context)

def student_applied_jobs(request):
    if not request.session.get('logged_in') or request.session.get('user_type') != 'student':
        return redirect('login')
    
    student = Student.objects.get(email=request.session['email'])
    applications = JobApplication.objects.filter(student=student).select_related('job')
    
    context = {
        'applications': applications,
    }
    return render(request, 'student_advanced/applied_jobs.html', context)

def student_profile(request):
    if not request.session.get('logged_in') or request.session.get('user_type') != 'student':
        return redirect('login')
    
    student = Student.objects.get(email=request.session['email'])
    profile, created = StudentProfile.objects.get_or_create(student=student)
    
    if request.method == 'POST':
        # Update basic student info from registration
        student.name = request.POST.get('name', student.name)
        student.phone_number = request.POST.get('phone_number', student.phone_number)
        student.branch = request.POST.get('branch', student.branch)
        student.year_of_study = request.POST.get('year_of_study', student.year_of_study)
        student.cgpa = request.POST.get('cgpa', student.cgpa)
        student.skills = request.POST.get('skills', student.skills)
        student.resume_link = request.POST.get('resume_link', student.resume_link)
        student.save()
        
        # Update advanced profile info
        profile.bio = request.POST.get('bio', '')
        profile.linkedin_url = request.POST.get('linkedin_url', '')
        profile.github_url = request.POST.get('github_url', '')
        profile.portfolio_url = request.POST.get('portfolio_url', '')
        profile.achievements = request.POST.get('achievements', '')
        profile.projects = request.POST.get('projects', '')
        profile.certifications = request.POST.get('certifications', '')
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('student_profile')
    
    context = {
        'student': student,
        'profile': profile,
    }
    return render(request, 'student_advanced/profile.html', context)

def apply_job(request, job_id):
    if not request.session.get('logged_in') or request.session.get('user_type') != 'student':
        return redirect('login')
    
    job = get_object_or_404(Job, id=job_id)
    student = Student.objects.get(email=request.session['email'])
    
    if JobApplication.objects.filter(student=student, job=job).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('student_jobs')
    
    application = JobApplication(
        student=student,
        job=job,
        cover_letter=request.POST.get('cover_letter', ''),
        resume_version=request.POST.get('resume_version', 'latest')
    )
    application.save()
    
    messages.success(request, f'Successfully applied for {job.title}!')
    return redirect('student_applied_jobs')