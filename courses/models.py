from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_trainer = models.BooleanField(default=False)

class Course(models.Model):
    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )
    title = models.CharField(max_length=255)
    Course_image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    description = models.TextField()
    pre_requisites = models.TextField(blank=True, null=True)
    course_outcomes = models.TextField(blank=True, null=True)
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='instructed_courses')
    duration = models.DurationField()
    level = models.CharField(max_length=15, choices=LEVEL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def duration_in_hours(self):
        total_seconds = self.duration.total_seconds()
        hours = total_seconds // 3600
        return f"{int(hours)} hours"
    def __str__(self):
        return self.title

class Enrollment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)

class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=255)
    video = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Progress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='progress')
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='progress')
    completed_at = models.DateTimeField(auto_now_add=True)

class Certificate(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    issue_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificate for {self.user.username} - {self.course.title}"

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    question = models.CharField(max_length=255)
    options = models.JSONField()  # Store options as a JSON object
    correct_option = models.CharField(max_length=255)

    def __str__(self):
        return self.question
    
class QuizAttempt(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=255)
    is_correct = models.BooleanField()

    class Meta:
        unique_together = ('user', 'quiz')