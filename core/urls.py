from django.urls import path
from . import views  # ✅ Make sure this line exists

urlpatterns = [
    path('', views.home, name='home'),
    path('assignments/', views.assignments, name='assignments'),
    path('quizzes/', views.quizzes, name='quizzes'),
    path('notices/', views.notices, name='notices'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cr-dashboard/', views.cr_dashboard, name='cr_dashboard'),
    path('upload-assignment/', views.upload_assignment, name='upload_assignment'),
    path('upload-quiz/', views.upload_quiz, name='upload_quiz'),
    path('upload-notice/', views.upload_notice, name='upload_notice'),
    path('cr-dashboard/', views.cr_dashboard, name='cr_dashboard'),
path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
path('edit-assignment/<int:assignment_id>/', views.edit_assignment, name='edit_assignment'),
path('edit-quiz/<int:quiz_id>/', views.edit_quiz, name='edit_quiz'),
path('assignment/<int:pk>/', views.assignment_detail, name='assignment_detail'),
path('quiz/<int:pk>/', views.quiz_detail, name='quiz_detail'),
path('notice/<int:pk>/', views.notice_detail, name='notice_detail'),
path('secret-migrate/', views.trigger_migrate, name='trigger_migrate'),




]
