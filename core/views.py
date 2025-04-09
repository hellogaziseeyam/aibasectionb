from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import date

from .forms import AssignmentForm, QuizForm, NoticeForm
from .models import Profile, Assignment, Quiz, Notice
from .decorators import role_required

# ✅ Role-aware Home View (fixes logo link issue)
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if hasattr(request.user, 'profile'):
        if request.user.profile.role == 'cr':
            return redirect('cr_dashboard')
        else:
            return redirect('student_dashboard')
    return redirect('student_dashboard')  # fallback

# ✅ Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if hasattr(user, 'profile') and user.profile.role == 'cr':
                return HttpResponseRedirect(reverse('cr_dashboard'))
            else:
                return HttpResponseRedirect(reverse('student_dashboard'))
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

# ✅ Logout
def logout_view(request):
    logout(request)
    return redirect('login')

# ✅ CR Dashboard
@role_required('cr')
def cr_dashboard(request):
    return render(request, 'core/cr_dashboard.html')

# ✅ Upload Assignment (CR only)
@role_required('cr')
def upload_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.created_by = request.user
            assignment.save()
            return redirect('assignments')
    else:
        form = AssignmentForm()
    return render(request, 'core/upload_assignment.html', {'form': form})

# ✅ Upload Quiz (CR only)
@role_required('cr')
def upload_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST, request.FILES)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()
            return redirect('quizzes')
    else:
        form = QuizForm()
    return render(request, 'core/upload_quiz.html', {'form': form})

# ✅ Upload Notice (CR only)
@role_required('cr')
def upload_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notices')
    else:
        form = NoticeForm()
    return render(request, 'core/upload_notice.html', {'form': form})

# ✅ Assignments Page
def assignments(request):
    all_assignments = Assignment.objects.all().order_by('due_date')
    return render(request, 'core/assignments.html', {'assignments': all_assignments})

# ✅ Quizzes Page
def quizzes(request):
    all_quizzes = Quiz.objects.all().order_by('date')
    return render(request, 'core/quizzes.html', {'quizzes': all_quizzes})

# ✅ Notices Page
def notices(request):
    all_notices = Notice.objects.all().order_by('-date')
    return render(request, 'core/notices.html', {'notices': all_notices})

# ✅ Student Dashboard
@login_required
def student_dashboard(request):
    notices = Notice.objects.all().order_by('-date')[:3]
    upcoming_assignments = Assignment.objects.filter(due_date__gte=date.today()).order_by('due_date')[:5]
    upcoming_quizzes = Quiz.objects.filter(date__gte=date.today()).order_by('date')[:5]

    return render(request, 'core/student_dashboard.html', {
        'notices': notices,
        'assignments': upcoming_assignments,
        'quizzes': upcoming_quizzes,
    })

# ✅ Edit Assignment (CR only)
@role_required('cr')
def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, created_by=request.user)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('assignments')
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'core/upload_assignment.html', {'form': form})

# ✅ Edit Quiz (CR only)
@role_required('cr')
def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)
    if request.method == 'POST':
        form = QuizForm(request.POST, request.FILES, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('quizzes')
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'core/upload_quiz.html', {'form': form})
