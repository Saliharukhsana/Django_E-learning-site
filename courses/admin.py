from django.contrib import admin
from .models import CustomUser, Course, Enrollment, Lecture, Progress, Certificate,Quiz

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_trainer')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'duration', 'level')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrollment_date')

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'video')

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lecture', 'completed_at')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'issue_date')
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ( 'course', 'question')