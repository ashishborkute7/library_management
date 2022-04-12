from django import forms
from django.contrib.auth.models import User
from . import models


class IssueBookForm(forms.Form):
    subject2 = forms.ModelChoiceField(queryset=models.Book.objects.all(), empty_label="Book Name [Subject]",
                                   to_field_name="subject", label="Book (Name and Subject)")
    name2 = forms.ModelChoiceField(queryset=models.Student.objects.all(), empty_label="Name [Branch] [Class] [Roll No]",
                                   to_field_name="user", label="Student Details")

    subject2.widget.attrs.update({'class': 'form-control'})
    name2.widget.attrs.update({'class': 'form-control'})
