# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('dashboard', '0004_task_progress'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_joined', models.DateField()),
                ('person', models.ForeignKey(to='authentication.UserProfile')),
                ('project', models.ForeignKey(to='dashboard.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(to='authentication.UserProfile', through='dashboard.Membership'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='member',
            field=models.ManyToManyField(to='authentication.UserProfile'),
            preserve_default=True,
        ),
    ]
