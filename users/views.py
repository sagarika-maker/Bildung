from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from .forms import SignUpForm
from courses.models import Course

from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages

def custom_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on role
            if user.role == "student":
                return redirect("student_dashboard")
            elif user.role == "instructor":
                return redirect("instructor_dashboard")
            else:
                return redirect("admin_dashboard")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "users/login.html")


# --- Signup ---
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
    return render(request, 'users/registration/signup.html', {'form': form})


# --- Login ---
class CustomLoginView(LoginView):
    template_name = "users/registration/login.html"

    def get_success_url(self):
        user = self.request.user
        if user.role == 'student':
            return "http://student.lvh.me:8000/"
        elif user.role == 'instructor':
            return "http://instructor.lvh.me:8000/"
        else:
            return "http://admin.lvh.me:8000/"


# --- Logout ---
def logout_view(request):
    logout(request)
    return redirect("login")


# --- Dashboards ---
def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.user.role == "student":
        return redirect("student_dashboard")
    elif request.user.role == "instructor":
        return redirect("instructor_dashboard")
    elif request.user.role == "admin":
        return redirect("admin_dashboard")


@login_required(login_url='/login/')
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('login')

    enrolled_courses = Course.objects.filter(enrollments__student=request.user)
    return render(request, 'courses/student_dashboard.html', {'enrolled_courses': enrolled_courses})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
#from .models import Course
#from .forms import CourseForm

@login_required(login_url='/login/')
def instructor_dashboard(request):
    if request.user.role != 'instructor':
        return redirect('login')

    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'courses/instructor_dashboard.html', {
        'courses': courses
    })


@login_required(login_url='/login/')
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('login')

    return render(request, 'admin/dashboard.html')

