from django.shortcuts import render
from dashboard.forms import ProjectForm,TaskForm
from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.sessions.models import Session
from django.contrib import messages
from dashboard.models import Project,Task,Membership
from authentication.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
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
				for member in unconf_members:
					m=Membership.objects.get(person=member)
					if not m.confirmed:
						l.append({'mempk':member.pk,'memname':member.user.first_name, 'memconf':m.confirmed, 'project':projects.name})
				print projects.members.all()
		pic_path= str(request.user.userprofile.picture)
		tasks=Task.objects.filter(member=request.user)
		context={'unconmem':l,'profile_pic': "/media/"+pic_path, 'username': request.user.first_name,'projects':project2,'tasks':tasks}
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
	member=UserProfile.objects.get(user=request.user)

	flag2=0
	flag=0
	if project.admin== request.user.username:
			flag=1
	try:
		mem=Membership.objects.get(person=member,project=project)
		if mem.confirmed == False:
			flag2=1
		else:
			flag=1
	except ObjectDoesNotExist as e:
		print "Not found"
		flag2=0
	
	print project.admin
	print request.user.username
		
	
		
	pic_path= str(project.project_img)
	tasks=Task.objects.filter(project=project)
	context={'profile_pic': "/media/"+pic_path,'project':project,'tasks':tasks, 'flag':flag,'flag2':flag2}
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
	context={'u':user1, 'project': adminproject, 'conproject':mem2, 'profile_pic2':profile_pic, 'profile_pic': "/media/"+pic_path, 'username': request.user.first_name}
	return render(request,"site/profile.html",context)


