from django.shortcuts import render
from dashboard.forms import ProjectForm
from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.sessions.models import Session
from django.contrib import messages
from dashboard.models import Project

# Create your views here.
def dashboard(request):
	# print request.user, request.user.is_active, request.user.is_authenticated()
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	else:
		projects=Project.objects.filter(admin=request.user.username)
		pic_path= str(request.user.userprofile.picture)
		context={'profile_pic': "/media/"+pic_path, 'username': request.user.first_name,'projects':projects}
		return render(request,'site/dashboard.html',context)


def addproject(request):
	if request.method == "POST":
		project_form=ProjectForm(data=request.POST)
		project=project_form.save(commit=False)
		project.admin=request.user.username
		project.project_img=request.FILES['project_img']
		project.save()
		return HttpResponseRedirect('/dashboard')
	else:
		project_form=ProjectForm()
		pic_path= str(request.user.userprofile.picture)
		context={'profile_pic': "/media/"+pic_path, 'username': request.user.first_name,'project_form':project_form}
	return render(request,'site/addproject.html',context)