# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='progress',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
