from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phoneNumber = models.CharField(max_length=30)
    collegeName = models.CharField(max_length=128)
    dateOfBirth = models.DateField()
    signUpDate = models.DateField(auto_now=True)
    picture = models.ImageField(upload_to='profile_pictures',blank=True)
    ipaddress = models.URLField(max_length=25)
    lastLoginDate = models.DateTimeField(blank=True)
    def __unicode__(self):
    	return self.user.first_name