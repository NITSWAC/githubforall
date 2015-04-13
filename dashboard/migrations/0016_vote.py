# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('dashboard', '0015_notification_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upordown', models.IntegerField()),
                ('post', models.ForeignKey(to='dashboard.Post')),
                ('user', models.ForeignKey(to='authentication.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
