"""
URL configuration for placement_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [

     # Advanced dashboards FIRST (before admin)
    path('student/advanced/', include('student_advanced.urls')),
    path('company/advanced/', include('company_advanced.urls')),
    path('admin/advanced/', include('admin_advanced.urls')),
    
    #THEN your main app
    path('admin/', admin.site.urls),
    path('', include('loginsystem.urls')),
    path('email/', include('emailverification.urls')),
]
