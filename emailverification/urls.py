from django.urls import path
from . import views
app_name = 'emailverification'

urlpatterns = [
    path('verify/', views.verify_otp, name='verify_otp'),
]