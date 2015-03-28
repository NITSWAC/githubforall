# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20150327_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='commit_msg',
            field=ckeditor.fields.RichTextField(default='Added first commit'),
            preserve_default=False,
        ),
    ]
