# core/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.http import HttpResponse

def home(request):
    return HttpResponse("Main Site - Bildung")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('forums/', include('forums.urls')),
    path('chat/', include('chat.urls')),

    # Login/logout for all users
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    path('', home),
]