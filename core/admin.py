from django.contrib import admin
from .models import Profile

admin.site.register(Profile)
from .models import Assignment, Quiz, Notice

admin.site.register(Assignment)
admin.site.register(Quiz)
admin.site.register(Notice)
