# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-16 03:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0019_auto_20170816_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='emailbot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.EmailBot'),
        ),
    ]
