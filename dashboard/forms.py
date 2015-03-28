from django import forms
from django.forms import widgets
from django.forms import ModelForm
from django.contrib.auth.models import User
from dashboard.models import Project,Task
from django.contrib import admin

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude=('admin',)
        fields=('name','max_members','desp','branch','project_img')

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude=('project',)
        fields=('name','desc','member')

