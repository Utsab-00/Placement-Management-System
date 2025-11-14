from django.contrib import admin
from .models import CompanyJob, Application, CompanyProfile

admin.site.register(CompanyJob)
admin.site.register(Application)
admin.site.register(CompanyProfile)