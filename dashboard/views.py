from django.shortcuts import render
from dashboard.forms import ProjectForm,TaskForm
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.sessions.models import Session
from django.contrib import messages
from dashboard.models import Project,Task,Membership,Commit
from authentication.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def load_defaults(request, context):
	pic_path= str(request.user.userprofile.picture)
	tasks=Task.objects.filter(member=request.user)
	userp=UserProfile.objects.get(user=request.user)
	context.update({'profile_pic': "/media/"+pic_path,'tasks':tasks,'userp':userp})

def dashboard(request):
	# print request.user, request.user.is_active, request.user.is_authenticated()
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	else:
		l=[]
		project2=Project.objects.filter(admin=request.user.username)
		if len(project2)>0:
			for projects in project2:
				unconf_members=projects.members.all()
				print unconf_members
				for member in unconf_members:
					print member
					m=Membership.objects.get(person=member,project=projects)
					if not m.confirmed:
						l.append({'mempk':member.pk,'memname':member.user.first_name, 'memconf':m.confirmed, 'project':projects})
				print projects.members.all()
		# pic_path= str(request.user.userprofile.picture)
		# tasks=Task.objects.filter(member=request.user)
		context={'unconmem':l,'projects':project2,}
		load_defaults(request,context)
		return render(request,'site/dashboard.html',context)


def addproject(request):
	if request.method == "POST":
		project_form=ProjectForm(data=request.POST)
		if project_form.is_valid():
			project=project_form.save(commit=False)
			project.admin=request.user.username
			project.project_img=request.FILES['project_img']
			project.save()
			return HttpResponseRedirect('/dashboard')
		else:
			# print user_form.errors, profile_form.errors
			# messages.clear()
			messages.error(request,str(project_form.errors))
	else:
		project_form=ProjectForm()
	# pic_path= str(request.user.userprofile.picture)
	# tasks=Task.objects.filter(member=request.user)
	context={'project_form':project_form,}
	load_defaults(request,context)
	return render(request,'site/addproject.html',context)



def addtask(request,project_id):
	project=Project.objects.get(pk=project_id)
	if request.method == "POST":
		task_form=TaskForm(data=request.POST)
		member_to_add=request.POST['member']
		commit=Commit()
		commit.project=project_id
		commit.user=request.user.username
		commit.commit_prog=0
		commit.commit_msg="Added new Task"
		commit.save()
		print 'printing member', member_to_add
		task=task_form.save(commit=False)
		task.progress=0
		task.last_commit=commit
		task.save()
		task.member.add(member_to_add)
		task.project.add(project)
		return HttpResponseRedirect('/dashboard')
	else:
		print request.user
		task_form=TaskForm()
		# pic_path= str(request.user.userprofile.picture)
		context={'project':project,'task_form':task_form,}
		return render(request,'site/addtask.html',context)

def viewproject(request,projectid):
	project=Project.objects.get(pk=projectid)
	member=UserProfile.objects.get(user=request.user)

	flag2=0
	flag=0
	role=""
	if project.admin== request.user.username:
			flag=1
			role="admin"
	try:
		mem=Membership.objects.get(person=member,project=project)
		if mem.confirmed == False:
			flag2=1
		else:
			flag=1
			role="member"
	except ObjectDoesNotExist as e:
		print "Not found"
		flag2=0
	project_members= Membership.objects.filter(project=project)
	print project.admin
	print request.user.username	
	pic_path= str(project.project_img)
	pic_path2=str(request.user.userprofile.picture)
	tasks=Task.objects.filter(project=project)
	context={'userp':member,'members':project_members, 'profile_pic': "/media/"+pic_path2,'profile_pic2': "/media/"+pic_path,'project':project,'tasks':tasks, 'flag':flag,'flag2':flag2,'role':role}
	return render(request,'site/viewproject.html',context)


def applytoproject(request,project_id):
	user=UserProfile.objects.get(user=request.user)
	project= Project.objects.get(pk=project_id)
	membership=Membership.objects.create(person=user, project=project)
	membership.save()
	return HttpResponseRedirect("/"+str(project_id)+"/viewproject")


def search(request):
	searchterm=request.GET['q'];
	projects=Project.objects.filter(name__startswith=searchterm)
	users=UserProfile.objects.filter(user__first_name__startswith=searchterm)
	pic_path= str(request.user.userprofile.picture)
	context={'projects': projects,'profile_pic': "/media/"+pic_path, 'username': request.user.first_name,'userlist':users}	
	return render(request,"site/search.html",context)

def profile(request,user_id):
	user1=UserProfile.objects.get(pk=user_id)
	adminproject=Project.objects.filter(admin=user1.user.username)
	mem=Membership.objects.filter(person=user1)
	mem2=[]
	for m in mem:
		if m.confirmed == True:
			mem2.append(m)
	profile_pic="/media/"+str(user1.picture)
	pic_path= str(request.user.userprofile.picture)
	context={'u':user1, 'project': adminproject, 'conproject':mem2, 'profile_pic2':profile_pic,}
	load_defaults(request,context)
	return render(request,"site/profile.html",context)

def accept(request,user_id,project_id):
	if request.user.username == Project.objects.get(pk=project_id).admin:
		print "Admin"
		project2= Project.objects.get(pk=project_id)
		user=UserProfile.objects.get(pk=user_id)
		mem=Membership.objects.get(person=user,project=project2)
		mem.confirmed=True
		mem.save()
		return HttpResponseRedirect('/dashboard')
	else:
		return HttpResponseRedirect('/logout')

def reject(request,user_id,project_id):
	if request.user.username == Project.objects.get(pk=project_id).admin:
		print "Admin"
		project2= Project.objects.get(pk=project_id)
		user=UserProfile.objects.get(pk=user_id)
		mem=Membership.objects.get(person=user,project=project2)
		mem.delete()
		return HttpResponseRedirect('/dashboard')
	else:
		return HttpResponseRedirect('/logout')

def tasks(request,user_id,project_id):
	userp=UserProfile.objects.get(pk=user_id)
	if request.user.username != userp.user.username:
		return HttpResponse("cant access- users dont match")
	project=Project.objects.get(pk=project_id)
	projects_administered= Project.objects.filter(admin=userp.user.username, pk=project_id)
	allowed_projects=Membership.objects.filter(person=userp, project=project)
	flag=False
	for p in allowed_projects:
		if p==p.project:
			flag=True
	if flag==True and project not in projects_administered:
		return HttpResponse("cant access- project cant be viewed")
	# projects_administered= Project.objects.filter(admin=userp.user.username, pk=project_id)
	# for p in projects_administered:
	# 	t=Task.objects.filter(project=p,member=userp)
	# 	t_list=[]
	# 	for task in t:
	# 		t_list.append(task)
	# 	project_tasks.update({p:t_list})
	# print project_tasks
	
	project_tasks=Task.objects.filter(project=project, member=userp)
	context={'project_tasks':project_tasks,'project':project}
	load_defaults(request,context)
	return render(request, 'site/tasks.html',context)


def updatetask(request, task_id,project_id):
	task=Task.objects.get(pk=task_id)
	members=task.member.all()
	flag=0 
	person=UserProfile.objects.get(user=request.user)
	print person.pk
	for m in members:
		if m==person:
			flag=1
			break;
	if flag == 1:
		print "Authenticated member"
		task.progress=request.POST['progress']
		commit=Commit()
		commit.project=project_id
		commit.user=request.user.username
		commit.commit_prog=request.POST['progress']
		commit.commit_msg=request.POST['commit_msg']
		commit.save()
		task.last_commit=commit
		task.save()


	return HttpResponseRedirect('/'+str(person.pk)+'-'+project_id+'/tasks')