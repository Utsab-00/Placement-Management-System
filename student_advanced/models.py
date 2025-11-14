from django.db import models
from django.utils import timezone
from loginsystem.models import Student  # Import from main app

class Job(models.Model):
    JOB_TYPE = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
    ]
    
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPE, default='full_time')
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100, blank=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} - {self.company_name}"

class JobApplication(models.Model):
    APPLICATION_STATUS = [
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('interview', 'Interview Scheduled'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='applied')
    cover_letter = models.TextField(blank=True)
    resume_version = models.CharField(max_length=100, blank=True)
    
    class Meta:
        unique_together = ['student', 'job']  # Prevent duplicate applications
    
    def __str__(self):
        return f"{self.student.name} - {self.job.title}"

class StudentProfile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    achievements = models.TextField(blank=True)
    projects = models.TextField(blank=True)
    certifications = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile - {self.student.name}"

class Interview(models.Model):
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE)
    interview_date = models.DateTimeField()
    interview_type = models.CharField(max_length=50)  # e.g., 'technical', 'hr'
    location = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    result = models.CharField(max_length=50, blank=True)  # e.g., 'passed', 'failed'
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Interview - {self.application.student.name}"