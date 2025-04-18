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
from django.http import HttpResponse
from django.core.management import call_command
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required  # optional: restrict to admin
def trigger_migrate(request):
    call_command('migrate')
    return HttpResponse("✅ Migrations applied.")


# ✅ Home View (based on user role)
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
    if request.user.is_authenticated:
        if hasattr(request.user, 'profile') and request.user.profile.role == 'cr':
            return redirect('cr_dashboard')
        else:
            return redirect('student_dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if hasattr(user, 'profile') and user.profile.role == 'cr':
                return redirect('cr_dashboard')
            else:
                return redirect('student_dashboard')
    else:
        form = AuthenticationForm()
        
    return render(request, 'core/login.html', {'form': form})

# ✅ Logout View
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
@login_required
def assignments(request):
    user_section = request.user.profile.section
    all_assignments = Assignment.objects.filter(section=user_section).order_by('due_date')
    return render(request, 'core/assignments.html', {'assignments': all_assignments})

# ✅ Quizzes Page
@login_required
def quizzes(request):
    user_section = request.user.profile.section
    all_quizzes = Quiz.objects.filter(section=user_section).order_by('date')
    return render(request, 'core/quizzes.html', {'quizzes': all_quizzes})

# ✅ Notices Page
@login_required
def notices(request):
    user_section = request.user.profile.section
    all_notices = Notice.objects.filter(section=user_section).order_by('-date')
    return render(request, 'core/notices.html', {'notices': all_notices})

# ✅ Student Dashboard
@login_required
def student_dashboard(request):
    section = request.user.profile.section
    notices = Notice.objects.filter(section=section).order_by('-date')[:3]
    upcoming_assignments = Assignment.objects.filter(section=section, due_date__gte=date.today()).order_by('due_date')[:5]
    upcoming_quizzes = Quiz.objects.filter(section=section, date__gte=date.today()).order_by('date')[:5]

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

# ✅ Detail Views
@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    return render(request, 'core/assignment_detail.html', {'assignment': assignment})

@login_required
def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    return render(request, 'core/quiz_detail.html', {'quiz': quiz})

@login_required
def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    return render(request, 'core/notice_detail.html', {'notice': notice})
