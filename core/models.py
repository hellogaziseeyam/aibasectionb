from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    ROLE_CHOICES = (
        ('cr', 'Class Representative'),
        ('student', 'Student'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

class Assignment(models.Model):
    course_name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    document = models.FileField(upload_to='assignment_docs/', blank=True, null=True)
    due_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course_name} - {self.title}"

    class Meta:
        ordering = ['-due_date']

class Quiz(models.Model):
    course_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    syllabus = models.TextField()
    document = models.FileField(upload_to='quiz_docs/', blank=True, null=True)
    date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.course_name}"

    class Meta:
        ordering = ['-date']

class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']
