# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-23 20:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('python_belt_exam_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='created_by',
        ),
    ]
