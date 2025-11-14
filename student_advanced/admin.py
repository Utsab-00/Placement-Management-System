from django.contrib import admin
from .models import Job, JobApplication, StudentProfile, Interview

admin.site.register(Job)
admin.site.register(JobApplication)
admin.site.register(StudentProfile)
admin.site.register(Interview)