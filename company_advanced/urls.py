from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.company_advanced_dashboard, name='company_advanced_dashboard'),
    path('post-jobs/', views.post_jobs, name='post_jobs'),
    path('applicants/', views.view_applicants, name='view_applicants'),
    path('update-application/<int:application_id>/', views.update_application_status, name='update_application_status'),
    path('profile/', views.company_profile, name='company_profile'),
]