from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'githubforall.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'authentication.views.index'),
    url(r'^login/', 'authentication.views._login'),
    url(r'^register/', 'authentication.views.register'),
    url(r'^loginuser/', 'authentication.views._loginuser'),
    url(r'^dashboard/', 'dashboard.views.dashboard'),
    url(r'^logout/', 'authentication.views._logout'),
    url(r'^addproject/','dashboard.views.addproject'),
    url(r'^(?P<project_id>\d+)/addtask/$', 'dashboard.views.addtask'),
    url(r'^(?P<projectid>\d+)/viewproject/$', 'dashboard.views.viewproject'),
    url(r'^(?P<project_id>\d+)/applytoproject/$', 'dashboard.views.applytoproject'),
    url(r'^search/$', 'dashboard.views.search'),
    url(r'^(?P<user_id>\d+)/profile/$', 'dashboard.views.profile'),
    url(r'^(?P<user_id>\d+)-(?P<project_id>\d+)/accept/$', 'dashboard.views.accept'),
    url(r'^(?P<user_id>\d+)-(?P<project_id>\d+)/reject/$', 'dashboard.views.reject'),
    url(r'^(?P<user_id>\d+)-(?P<project_id>\d+)/tasks/$', 'dashboard.views.tasks'),
    url(r'^(?P<task_id>\d+)-(?P<project_id>\d+)/updatetask/$', 'dashboard.views.updatetask'),
    url(r'^newthread/','dashboard.views.newthread'),
    (r'^ckeditor/', include('ckeditor.urls')),
    url(r'^th/(?P<thread_id>\d+)/$', 'dashboard.views.thread'),
    url(r'^th/(?P<thread_id>\d+)-(?P<post_id>\d+)/upvote/$', 'dashboard.views.upvote'),
    url(r'^th/(?P<thread_id>\d+)-(?P<post_id>\d+)/downvote/$', 'dashboard.views.downvote'),
    url(r'^(?P<user_id>\d+)/alltasks/$', 'dashboard.views.alltasks'),



)

from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
)