# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_remove_task_commit_msg'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project', models.IntegerField()),
                ('user', models.CharField(max_length=100)),
                ('commit_prog', models.IntegerField()),
                ('commit_msg', models.TextField()),
                ('commit_date', models.DateField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='task',
            name='last_commit',
            field=models.ForeignKey(default=1, to='dashboard.Commit'),
            preserve_default=False,
        ),
    ]
