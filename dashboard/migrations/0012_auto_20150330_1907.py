# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_auto_20150330_1817'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='thread_started_by',
            new_name='thread',
        ),
    ]
