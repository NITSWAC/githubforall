# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 5, 5, 29, 49, 735224, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
