# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_auto_20150330_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='downvotes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='upvotes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
