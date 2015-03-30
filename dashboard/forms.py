from django import forms
from django.forms import widgets
from django.forms import ModelForm
from django.contrib.auth.models import User
from dashboard.models import Project,Task,Thread,Post
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

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

class ThreadForm(forms.ModelForm):
	class Meta:
		model=Thread
		exclude=('started_by', 'posted_at', 'members_posted')
		fields=('msg','heading')

class PostForm(forms.ModelForm):
	class Meta:
		model=Post
		exclude=('thread','posted_at','posted_at')
		fields=('msg',)
