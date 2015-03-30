from django.contrib import admin
from dashboard.models import *

# Register your models here.
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Membership)
admin.site.register(Commit)
admin.site.register(Thread)
admin.site.register(Post)