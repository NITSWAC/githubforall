# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_task_commit_msg'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='commit_msg',
        ),
    ]
