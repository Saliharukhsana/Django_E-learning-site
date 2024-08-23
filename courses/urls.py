from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('courses/', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('progress/', views.progress, name='progress'),
    path('profile/', views.profile, name='profile'),
    path('enroll/<int:course_id>/', views.enroll_now, name='enroll_now'),
    path('course/<int:course_id>/quiz/', views.quiz_page, name='quiz_page'),
]

