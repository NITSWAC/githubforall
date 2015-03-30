# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('dashboard', '0010_auto_20150328_0531'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('posted_at', models.DateTimeField(auto_now=True)),
                ('msg', models.TextField()),
                ('posted_by', models.ForeignKey(to='authentication.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('heading', models.CharField(max_length=100)),
                ('msg', models.TextField()),
                ('posted_at', models.DateTimeField(auto_now=True)),
                ('members_posted', models.ManyToManyField(to='authentication.UserProfile', through='dashboard.Post')),
                ('started_by', models.ForeignKey(related_name='thread_requests_created', to='authentication.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='thread_started_by',
            field=models.ForeignKey(to='dashboard.Thread'),
            preserve_default=True,
        ),
    ]
