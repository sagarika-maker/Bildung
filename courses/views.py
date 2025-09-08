from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment
from django.contrib import messages

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, "courses/course_list.html", {"courses": courses})


@login_required
def create_course(request):
    if request.user.role != "instructor":
        messages.error(request, "Only instructors can create courses.")
        return redirect("course_list")

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        course = Course.objects.create(instructor=request.user, title=title, description=description)
        messages.success(request, "Course created successfully.")
        return redirect("course_list")

    return render(request, "courses/create_course.html")


@login_required
def enroll_course(request, course_id):
    if request.user.role != "student":
        messages.error(request, "Only students can enroll.")
        return redirect("course_list")

    course = get_object_or_404(Course, id=course_id)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    messages.success(request, f"Enrolled in {course.title}.")
    return redirect("course_list")
