# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-13 12:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_auto_20170913_2140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testcase',
            name='binaryName',
        ),
    ]