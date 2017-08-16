# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-16 03:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0018_auto_20170816_0108'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailbot',
            name='email_pw_enc',
            field=models.CharField(default='', max_length=512),
        ),
        migrations.AlterField(
            model_name='emailbot',
            name='email_pw',
            field=models.CharField(blank=True, help_text='Use only if you want to change password', max_length=512, null=True),
        ),
    ]
