from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Project(models.Model):
	admin=models.CharField(max_length=100)
	name=models.CharField(max_length=100)
	max_members=models.IntegerField()
	desp=models.TextField()
	branch=models.CharField(max_length=100)
	createdate=models.DateField(auto_now=True)
	project_img=models.ImageField(upload_to='project_img',blank=True)
	def __str__(self):
		return self.name
class Task(models.Model):
	project=models.ManyToManyField(Project)
	name=models.CharField(max_length=100)
	member= models.ManyToManyField(User)
	desc=models.TextField()    