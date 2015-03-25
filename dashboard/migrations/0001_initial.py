# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('admin', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('max_members', models.IntegerField()),
                ('desp', models.TextField()),
                ('branch', models.CharField(max_length=100)),
                ('project_img', models.ImageField(upload_to=b'project_img', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
