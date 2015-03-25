from django.db import models

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
    