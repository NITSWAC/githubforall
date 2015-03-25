# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0002_project_createdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('desc', models.TextField()),
                ('member', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('project', models.ManyToManyField(to='dashboard.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
