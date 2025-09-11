from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.custom_login, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('instructor/dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]