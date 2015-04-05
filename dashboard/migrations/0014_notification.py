# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('dashboard', '0013_auto_20150331_1156'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('msg_type', models.CharField(max_length=2, choices=[(b'AT', b'Added Task'), (b'UT', b'Updated Task'), (b'AP', b'Accepted Project'), (b'RP', b'Rejected Project'), (b'Applied', b'Applied to your Project'), (b'UP', b'upvoted your comment'), (b'DW', b'Downvoted your comment'), (b'PO', b'Someone posted on your thread')])),
                ('msg', models.CharField(max_length=50)),
                ('clicked', models.BooleanField(default=False)),
                ('link', models.URLField()),
                ('member', models.ForeignKey(to='authentication.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
