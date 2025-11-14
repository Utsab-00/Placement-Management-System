from django.contrib import admin
from .models import PlacementReport, SystemAnalytic, Announcement, PlacementDrive, ContactMessage

admin.site.register(PlacementReport)
admin.site.register(SystemAnalytic)
admin.site.register(Announcement)
admin.site.register(PlacementDrive)
admin.site.register(ContactMessage)