from django.db import models
from django.contrib.auth.models import User
from authentication.models import UserProfile
from ckeditor.fields import RichTextField
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

# tag feature and a category model
class Thread(models.Model):
	started_by = models.ForeignKey(UserProfile,related_name='%(class)s_requests_created')
	heading = models.CharField(max_length=100)
	msg= models.TextField()
	posted_at =models.DateTimeField(auto_now=True)
	members_posted = models.ManyToManyField(UserProfile, through='Post')
	def __str__(self):
		return self.heading




class Post(models.Model):
	thread = models.ForeignKey(Thread)
	posted_by = models.ForeignKey(UserProfile)
	posted_at =models.DateTimeField(auto_now=True)
	msg=models.TextField()
	upvotes=models.IntegerField(default=0)
	downvotes=models.IntegerField(default=0)
	def __str__(self):
		return self.posted_by.user.first_name + " " + self.msg[:50] +"..."

class Notification(models.Model):
	NOTIFICATION_CHOICES = (
    ('AT', 'Added Task'),
    ('UT', 'Updated Task'),
    ('AP', 'Accepted Project'),
    ('RP', 'Rejected Project'),
    ('Applied', 'Applied to your Project'),
    ('UP', 'upvoted your comment'),
    ('DW', 'Downvoted your comment'),
    ('PO', 'Someone posted on your thread'),
	)	
	member=models.ForeignKey(UserProfile)
	msg_type = models.CharField(max_length=2, choices=NOTIFICATION_CHOICES)
	msg = models.CharField(max_length=50)
	clicked = models.BooleanField(default = False)
	link = models.URLField()
	created_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.member.user.first_name + " " + self.msg[:50] +"..."

