from django.contrib import admin
from dashboard.models import Project,Task,Membership

# Register your models here.
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Membership)