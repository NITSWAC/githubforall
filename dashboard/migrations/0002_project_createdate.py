# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='createdate',
            field=models.DateField(default=datetime.datetime(2015, 3, 25, 15, 25, 37, 456587, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
