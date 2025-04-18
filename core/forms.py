from django import forms
from .models import Assignment, Quiz, Notice

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['course_name', 'title', 'description', 'document', 'due_date']  # 🔁 No 'section'

    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)

        self.fields['course_name'].widget = forms.Select(
            choices=self.fields['course_name'].choices,
            attrs={'class': 'form-control'}
        )

        for field_name, field in self.fields.items():
            if field_name != 'course_name':
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = f'Enter {field.label}'


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['course_name', 'title', 'syllabus', 'document', 'date']  # 🔁 No 'section'

    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)

        self.fields['course_name'].widget = forms.Select(
            choices=self.fields['course_name'].choices,
            attrs={'class': 'form-control'}
        )

        for field_name, field in self.fields.items():
            if field_name != 'course_name':
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = f'Enter {field.label}'


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super(NoticeForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = f'Enter {field.label}'
