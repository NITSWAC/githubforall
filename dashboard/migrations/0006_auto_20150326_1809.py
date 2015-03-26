# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20150326_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='confirmed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membership',
            name='date_joined',
            field=models.DateField(auto_now=True),
            preserve_default=True,
        ),
    ]
