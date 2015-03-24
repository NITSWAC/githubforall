from django.shortcuts import render
from authentication.forms import UserForm,UserProfileForm
from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.sessions.models import Session
from django.contrib import messages

# Create your views here.
def dashboard(request):
	# print request.user, request.user.is_active, request.user.is_authenticated()
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login')
	else:
		pic_path= str(request.user.userprofile.picture)
		context={'profile_pic': "/media/"+pic_path, 'username': request.user.first_name}
		return render(request,'site/dashboard.html',context)