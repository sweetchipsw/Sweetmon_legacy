# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Crash',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('crash_hash', models.CharField(max_length=200)),
                ('fuzzer_name', models.CharField(max_length=200)),
                ('target', models.CharField(max_length=200)),
                ('reg_date', models.DateTimeField(verbose_name=b'date published')),
                ('link', models.CharField(max_length=1000)),
                ('abstract', models.CharField(max_length=6553500)),
                ('dup_crash', models.IntegerField(default=0)),
                ('comment', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=100)),
                ('fuzzer_name', models.CharField(max_length=50)),
                ('pub_ip', models.CharField(max_length=16)),
                ('pri_ip', models.CharField(max_length=16)),
                ('reg_date', models.DateTimeField(verbose_name=b'date published')),
                ('crash', models.IntegerField(default=0)),
                ('testcase', models.IntegerField(default=0)),
                ('ping', models.IntegerField(default=0)),
            ],
        ),
    ]
