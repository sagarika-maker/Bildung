from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log in the user after signup

            # redirect based on role
            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'instructor':
                return redirect('instructor_dashboard')
            else:
                return redirect('admin_dashboard')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})



from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.role == 'student':
            return 'http://student.lvh.me:8000/'
        elif user.role == 'instructor':
            return 'http://instructor.lvh.me:8000/'
        else:
            return 'http://admin.lvh.me:8000/'

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "users/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.user.role == "student":
        return render(request, "users/student_dashboard.html")
    elif request.user.role == "instructor":
        return render(request, "users/instructor_dashboard.html")
    elif request.user.role == "admin":
        return render(request, "users/admin_dashboard.html")


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from courses.models import Course

@login_required(login_url='/login/')
def student_dashboard(request):
    print("Student dashboard view called!")
    # Ensure only students access this view
    if request.user.role != 'student':
        return redirect('login')
    
    courses = Course.objects.filter(enrollment__student=request.user)
    return render(request, 'student/dashboard.html', {'courses': courses})


@login_required(login_url='/login/')
def instructor_dashboard(request):
    print("instructor  dashboard view called!")
    if request.user.role != 'instructor':
        return redirect('login')
    
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'instructor/dashboard.html', {'courses': courses})


@login_required(login_url='/login/')
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('login')
    
    # Admin-specific logic
    return render(request, 'admin/dashboard.html')

