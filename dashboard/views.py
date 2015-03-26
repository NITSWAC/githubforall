from django.shortcuts import render
from dashboard.forms import ProjectForm,TaskForm
from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.sessions.models import Session
from django.contrib import messages
from dashboard.models import Project,Task

# Create your views here.
def dashboard(request):
	# print request.user, request.user.is_active, request.user.is_authenticated()
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	else:
		projects=Project.objects.filter(admin=request.user.username)
		pic_path= str(request.user.userprofile.picture)
		tasks=Task.objects.filter(member=request.user)
		context={'profile_pic': "/media/"+pic_path, 'username': request.user.first_name,'projects':projects,'tasks':tasks}
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
		tasks=Task.objects.filter(member=request.user)
		context={'profile_pic': "/media/"+pic_path, 'username': request.user.first_name,'project_form':project_form,'tasks':tasks}
	return render(request,'site/addproject.html',context)



def addtask(request,project_id):
	project=Project.objects.get(pk=project_id)
	if request.method == "POST":
		task_form=TaskForm(data=request.POST)
		member_to_add=request.POST['member']

		print 'printing member', member_to_add
		task=task_form.save(commit=False)
		task.save()
		task.member.add(member_to_add)
		task.project.add(project)
		return HttpResponseRedirect('/dashboard')
	else:
		print request.user
		task_form=TaskForm()
		pic_path= str(request.user.userprofile.picture)
		context={'project':project,'task_form':task_form,'profile_pic': "/media/"+pic_path, 'username': request.user.first_name}
		return render(request,'site/addtask.html',context)

def viewproject(request,projectid):
	project=Project.objects.get(pk=projectid)
	flag=0
	print project.admin
	print request.user.username
	if project.admin== request.user.username:
		flag=1
	pic_path= str(request.user.userprofile.picture)
	tasks=Task.objects.filter(project=project)
	context={'profile_pic': "/media/"+pic_path,'project':project,'tasks':tasks, 'flag':flag}
	return render(request,'site/viewproject.html',context)


