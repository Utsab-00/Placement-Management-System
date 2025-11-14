from django.db import models
from loginsystem.models import Company, Student  # Import from main app

class CompanyJob(models.Model):
    JOB_TYPE = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPE, default='full_time')
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    posted_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()
    is_active = models.BooleanField(default=True)
    vacancies = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.title} - {self.company.company_name}"

class Application(models.Model):
    APPLICATION_STATUS = [
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('interview', 'Interview Scheduled'),
    ]
    
    job = models.ForeignKey(CompanyJob, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='applied')
    company_notes = models.TextField(blank=True)
    rating = models.IntegerField(default=0)  # Company's rating of applicant (1-5)
    
    class Meta:
        unique_together = ['job', 'student']  # Prevent duplicate applications
    
    def __str__(self):
        return f"{self.student.name} - {self.job.title}"

class CompanyProfile(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    founded_year = models.IntegerField(blank=True, null=True)
    company_size = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    social_links = models.TextField(blank=True)  # JSON or comma-separated
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile - {self.company.company_name}"