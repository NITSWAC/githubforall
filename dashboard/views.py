from django.shortcuts import render
from dashboard.forms import ProjectForm,TaskForm,ThreadForm,PostForm
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.sessions.models import Session
from django.contrib import messages
from dashboard.models import Project,Task,Membership,Commit,Thread,Post
from authentication.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist
import json

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
		userp=UserProfile.objects.get(user=request.user)
		threads_started=Thread.objects.filter(started_by=userp)
		m={}
		for t in threads_started:
			k=len(Post.objects.filter(thread=t))
			m[t]=k


		context={'unconmem':l,'projects':project2,'threads_started':threads_started,'myposts': m}
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

	project_members= Membership.objects.filter(project=project, confirmed=True)
	unconfirmed_members=Membership.objects.filter(project=project, confirmed=False)

	print project.admin
	print request.user.username	
	pic_path= str(project.project_img)
	pic_path2=str(request.user.userprofile.picture)
	tasks=Task.objects.filter(project=project)
	context={'unconmem':unconfirmed_members,'userp':member,'members':project_members, 'profile_pic': "/media/"+pic_path2,'profile_pic2': "/media/"+pic_path,'project':project,'tasks':tasks, 'flag':flag,'flag2':flag2,'role':role}
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

def newthread(request):
	userp= UserProfile.objects.get(user=request.user)
	if request.method =='POST':
		thread_form=ThreadForm(data=request.POST)
		if thread_form.is_valid():
			thread=thread_form.save(commit=False)
			thread.started_by=userp
			thread.save()
			return HttpResponseRedirect('/dashboard')
		else:
			# print user_form.errors, profile_form.errors
			# messages.clear()
			messages.error(request,str(thread_form.errors))
	else:
		thread_form=ThreadForm()
	context={'thread_form':thread_form}
	load_defaults(request,context)
	return render(request, 'site/newthread.html',context)	

def thread(request,thread_id):
	userp= UserProfile.objects.get(user=request.user)
	thread=Thread.objects.get(pk=thread_id)
	posts=Post.objects.filter(thread=thread)
	
	# if request.method =='POST':
	# 	post_form=PostForm(data=request.POST)
	# 	if post_form.is_valid():
	# 		post=post_form.save(commit=False)
	# 		post.posted_by=userp
	# 		post.thread=thread
	# 		post.save()
	# 		# return HttpResponseRedirect('/th/'+str(thread_id))
	# 	else:
	# 		messages.error(request,str(post_form.errors))
	post_form=PostForm()
	context={'thread':thread, 'posts':posts,'post_form':post_form}
	load_defaults(request,context)
	return render(request, 'site/thread.html', context)

def create_post(request,thread_id):
    if request.method == 'POST':
    	print 'in view'
        post_text = request.POST.get('the_post')
        print post_text
        # post_text= request.POST['the_post']
        thread=Thread.objects.get(pk=thread_id)
        response_data = {}
        userp= UserProfile.objects.get(user=request.user)
        post = Post(msg=post_text, posted_by=userp, thread=thread)
        post.save()
        response_data['result'] = 'Create post successful!'
        response_data['postpk'] = post.pk
        response_data['text'] = post.msg
        response_data['created'] = post.posted_at.strftime('%B %d, %Y %I:%M %p')
        response_data['author'] = post.posted_by.user.first_name
        response_data['pic_path']= "/media/"+str(post.posted_by.user.userprofile.picture)
        response_data['thread_id']=thread_id

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
def upvote(request,post_id,thread_id):
	post=Post.objects.get(pk=post_id)
	if request.user.is_authenticated():
		post.upvotes=post.upvotes+1
		post.save()
	return HttpResponseRedirect('/th/'+str(thread_id))

def downvote(request,post_id,thread_id):
	post=Post.objects.get(pk=post_id)
	if request.user.is_authenticated():
		post.downvotes=post.downvotes+1
		post.save()
	return HttpResponseRedirect('/th/'+str(thread_id))

def alltasks(request,user_id):
	userp=UserProfile.objects.get(pk=user_id)
	if request.user.username != userp.user.username:
		return HttpResponse("cant access- users dont match")
	project_tasks=Task.objects.filter(member=userp)
	context={'project_tasks':project_tasks,'project':project}
	load_defaults(request,context)
	return render(request, 'site/alltasks.html',context)

def upvote2(request):
	upvotes=0
	if request.method == 'GET':
		post_id=request.GET['post_id']
		thread_id=request.GET['thread_id']
		post=Post.objects.get(pk=post_id)
		if request.user.is_authenticated():
			post.upvotes=post.upvotes+1
			upvotes=post.upvotes
			post.save()
	return HttpResponse(upvotes)

def downvote2(request):
	downvotes=0
	if request.method == 'GET':
		post_id=request.GET['post_id']
		thread_id=request.GET['thread_id']
		post=Post.objects.get(pk=post_id)
		if request.user.is_authenticated():
			post.downvotes=post.downvotes+1
			downvotes=post.downvotes
			post.save()
	return HttpResponse(downvotes)
