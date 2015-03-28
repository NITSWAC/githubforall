from django.db import models
from django.contrib.auth.models import User
from authentication.models import UserProfile
# Create your models here.


class Project(models.Model):
	admin=models.CharField(max_length=100)
	name=models.CharField(max_length=100,unique=True)
	max_members=models.IntegerField()
	desp=models.TextField()
	branch=models.CharField(max_length=100)
	createdate=models.DateField(auto_now=True)
	project_img=models.ImageField(upload_to='project_img',blank=True)
	members=models.ManyToManyField(UserProfile, through='Membership')
	def __str__(self):
		return self.name

class Membership(models.Model):
	person = models.ForeignKey(UserProfile)
	project = models.ForeignKey(Project)
	date_joined = models.DateField(auto_now=True)
	confirmed = models.BooleanField(default=False)


class Commit(models.Model):
	project=models.IntegerField()
	user=models.CharField(max_length=100)
	commit_prog=models.IntegerField()
	commit_msg=models.TextField()
	commit_date=models.DateField(auto_now=True)
	def __str__(self):
		return self.commit_msg

class Task(models.Model):
	project=models.ManyToManyField(Project)
	name=models.CharField(max_length=100)
	member= models.ManyToManyField(UserProfile)
	desc=models.TextField()    
	progress= models.IntegerField()
	last_commit=models.ForeignKey(Commit)
	def __str__(self):
		return self.name