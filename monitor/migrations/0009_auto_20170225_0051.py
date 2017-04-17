# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0008_crash_crash_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('idx', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1024)),
                ('link', models.CharField(max_length=1024)),
                ('isopen', models.BooleanField(default=True)),
                ('cve', models.CharField(max_length=200)),
                ('etc_numbering', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Testcase',
            fields=[
                ('idx', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('target', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1024)),
                ('testcase_file', models.FileField(upload_to='', storage=django.core.files.storage.FileSystemStorage(location='/home/sweetchip/sweetboard/sweetmon/private'))),
                ('testcase_size', models.IntegerField(default=0)),
                ('link', models.CharField(max_length=1024)),
            ],
        ),
        migrations.AddField(
            model_name='crash',
            name='isopen',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='crash',
            name='crash_file',
            field=models.FileField(upload_to='', storage=django.core.files.storage.FileSystemStorage(location='/home/sweetchip/sweetboard/sweetmon/private')),
        ),
    ]
