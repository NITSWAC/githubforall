from django.shortcuts import render
from authentication.forms import UserForm,UserProfileForm
from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.sessions.models import Session
from django.contrib import messages
# Create your views here.
def index(request):
	if request.user.is_authenticated():
		print "is authenticated"
		return HttpResponseRedirect('/dashboard/')
	else:
		return HttpResponseRedirect('/login')



def _login(request):
	title="Login"
	return render(request,'site/login.html',{'title':title})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def _loginuser(request):
	if request.method=="POST":
		username=request.POST.get('email',False)
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(username=email, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				user.lastLoginDate=datetime.now()
				user.save()
				if not request.POST.get('remember_me', None):
					request.session.set_expiry(0)
				messages.info(request,'Welcome '+user.username)
				request.session['username']=email
				request.session['loggedin']=1
				return HttpResponseRedirect('/')
			else:
				messages.info(request,'Your account is inactive. Contact webmaster')
				return HttpResponseRedirect('/login')
		else:
			messages.error(request,'Invalid username/password')
			return HttpResponseRedirect('/login')

def register(request):	
	registered = False
	if request.method == "POST":
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		print profile_form
		print request.FILES['picture']
		if user_form.is_valid() and profile_form.is_valid():
			print "Got in"
			
			user = user_form.save(commit=False)
			user.set_password(user.password)
			user.is_active=True
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			profile.lastLoginDate = datetime.now()
			profile.ipaddress=get_client_ip(request)
			if request.FILES['picture']:
				profile.picture = request.FILES['picture']
			profile.save()
			registered = True
		else:
			print user_form.errors, profile_form.errors
			messages.info(request,str(user_form.errors)+str(profile_form.errors))
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
	return render(request,'site/register.html',{'title':'Sign Up','current_page':'register',\
		'user_form':user_form,'profile_form':profile_form,'registered':registered})


# def dashboard(request):
# 	try:
# 		if request.session['loggedin'] == 1:
# 			return render(request,'site/dashboard.html')
# 	except KeyError:
# 		return HttpResponseRedirect('/login')

# def dashboard(request):
# 	# print request.user, request.user.is_active, request.user.is_authenticated()
# 	if not request.user.is_authenticated():
# 		return HttpResponseRedirect('/login')
# 	else:
# 		pic_path= str(request.user.userprofile.picture)
# 		context={'profile_pic': "/media/"+pic_path}
# 		return render(request,'site/dashboard.html',context)


def _logout(request):
	print request.user.username
	# del request.session['loggedin']
	# del request.session['username']
	logout(request)
	return HttpResponseRedirect('/login')