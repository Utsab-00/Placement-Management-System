from django.db import models
from django.utils import timezone
from loginsystem.models import Student, Company  # Import from main app

class PlacementReport(models.Model):
    REPORT_TYPE = [
        ('monthly', 'Monthly Report'),
        ('yearly', 'Yearly Report'),
        ('placement', 'Placement Drive Report'),
        ('custom', 'Custom Report'),
    ]
    
    report_title = models.CharField(max_length=200)
    generated_date = models.DateTimeField(auto_now_add=True)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE)
    data = models.JSONField(default=dict)  # Store report data as JSON
    generated_by = models.CharField(max_length=100)
    file_path = models.FileField(upload_to='reports/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.report_title} - {self.generated_date.strftime('%Y-%m-%d')}"

class SystemAnalytic(models.Model):
    metric_name = models.CharField(max_length=100)
    metric_value = models.JSONField(default=dict)
    recorded_date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.metric_name} - {self.recorded_date}"

class Announcement(models.Model):
    TARGET_AUDIENCE = [
        ('all', 'All Users'),
        ('students', 'Students Only'),
        ('companies', 'Companies Only'),
        ('admins', 'Admins Only'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    target_audience = models.CharField(max_length=20, choices=TARGET_AUDIENCE, default='all')
    created_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.title} - {self.target_audience}"

class PlacementDrive(models.Model):
    drive_name = models.CharField(max_length=200)
    companies = models.ManyToManyField(Company, blank=True)
    participating_students = models.ManyToManyField(Student, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.drive_name

class ContactMessage(models.Model):
    MESSAGE_STATUS = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('closed', 'Closed'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=MESSAGE_STATUS, default='new')
    received_date = models.DateTimeField(auto_now_add=True)
    admin_notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.subject} - {self.name}"