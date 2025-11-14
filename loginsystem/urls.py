from django.urls import path
from . import views 
from .views import login_view
 # Import views from the same app

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('companies/', views.company_list, name='company_list'),
    path('admins/', views.admin_list, name='admin_list'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('admin_view/', views.admin_page, name="admin"),
    path('company_view/', views.company_page, name="company"),
    path('student_view/', views.student_page, name="student"),

    # NEW: Advanced dashboard redirect
    path('advanced-dashboard/', views.redirect_to_advanced_dashboard, name="advanced_dashboard"),
]
