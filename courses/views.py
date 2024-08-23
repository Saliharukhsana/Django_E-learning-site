from itertools import count
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, Lecture, Progress, Certificate,Quiz,QuizAttempt
from .forms import CustomUserCreationForm,QuizForm
from .forms import LoginForm
from django.db.models import Count
from django.forms import modelformset_factory
from django.core.paginator import Paginator
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('course_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'courses/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('course_list')
    else:
        form = LoginForm()
    return render(request, 'courses/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('course_list')

@login_required(login_url='login')
def course_list(request):
    query = request.GET.get('q', '')
    level = request.GET.get('level', '')
    page_number = request.GET.get('page', 1)

    courses = Course.objects.all()

    if query:
        courses = courses.filter(title__icontains=query)
    
    if level:
        courses = courses.filter(level=level)
    courses = courses.annotate(enrollment_count=Count('enrollments'))
    paginator = Paginator(courses,9)  # Show 10 courses per page
    page_obj = paginator.get_page(page_number)
    return render(request, 'courses/course_list.html', { 'courses': page_obj, 'query': query})

def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    lectures = course.lectures.all()
    is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists() if request.user.is_authenticated else False
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lectures': lectures,
        'is_enrolled': is_enrolled
    })

@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    return redirect('course_detail', course_id=course_id)

@login_required
def progress(request):
    user_progress = Progress.objects.filter(user=request.user)
    return render(request, 'courses/progress.html', {'progress': user_progress})

@login_required
def profile(request):
    user_courses = request.user.enrollments.all()
    return render(request, 'courses/profile.html', {'user_courses': user_courses})

from django.shortcuts import redirect, get_object_or_404

@login_required
def enroll_now(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)

    if created:
        # The user was not enrolled and is now enrolled
        message = "You have successfully enrolled in the course."
    else:
        # The user is already enrolled
        message = "You are already enrolled in this course."

    # Fetch all lectures related to this course
    lectures = course.lectures.all()
    print(lectures)
    return render(request, 'courses/course_content.html', {'course': course,'lectures': lectures,'message': message})
@login_required
def quiz_page(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    quizzes = Quiz.objects.filter(course=course)
    QuizAttemptFormSet = modelformset_factory(QuizAttempt, form=QuizForm, extra=0, can_delete=False)

    if request.method == 'POST':
        formset = QuizAttemptFormSet(request.POST, queryset=QuizAttempt.objects.none())
        if formset.is_valid():
            for form in formset:
                quiz_attempt = form.save(commit=False)
                quiz_attempt.user = request.user
                quiz_attempt.is_correct = quiz_attempt.selected_option == quiz_attempt.quiz.correct_option
                quiz_attempt.save()
            return redirect('quiz_results', course_id=course_id)
    else:
        # Initialize the formset with empty QuizAttempt instances, associating them with each quiz
        initial_data = [{'quiz': quiz} for quiz in quizzes]
        formset = QuizAttemptFormSet(queryset=QuizAttempt.objects.none(), initial=initial_data)

    return render(request, 'courses/quiz_page.html', {'course': course, 'formset': formset})
