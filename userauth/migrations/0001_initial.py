# -*- coding: utf-8 -*-
# Generated by Django 1.10.dev20160310155155 on 2016-05-07 08:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=20, unique=True)),
                ('user_type', models.CharField(max_length=20)),
            ],
        ),
    ]
