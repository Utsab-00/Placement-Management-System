from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_advanced_dashboard, name='admin_advanced_dashboard'),
    path('manage-students/', views.manage_students, name='manage_students'),
    path('manage-companies/', views.manage_companies, name='manage_companies'),
    path('manage-jobs/', views.manage_jobs, name='manage_jobs'),
    path('toggle-verification/<str:user_type>/<int:user_id>/', views.toggle_verification, name='toggle_verification'),
    path('profile/', views.admin_profile, name='admin_profile'),
]