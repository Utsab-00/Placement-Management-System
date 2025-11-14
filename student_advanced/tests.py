from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_advanced_dashboard'),
    path('jobs/', views.student_jobs, name='student_jobs'),
    path('applied-jobs/', views.student_applied_jobs, name='student_applied_jobs'),
    path('profile/', views.student_profile, name='student_profile'),
    path('apply-job/<int:job_id>/', views.apply_job, name='apply_job'),
]