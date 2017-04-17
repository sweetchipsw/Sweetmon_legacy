# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage
import monitor.models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0009_auto_20170225_0051'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnetimeToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=512)),
                ('real_path', models.CharField(max_length=5120)),
            ],
        ),
        migrations.RemoveField(
            model_name='testcase',
            name='link',
        ),
        migrations.RemoveField(
            model_name='testcase',
            name='testcase_file',
        ),
        migrations.AddField(
            model_name='issue',
            name='reward',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='testcase',
            name='fuzzer_url',
            field=models.CharField(max_length=1024, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='testcase',
            name='testcase_url',
            field=models.CharField(default='', max_length=1024),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='crash',
            name='crash_file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location=b'/home/sweetchip/sweetboard/sweetmon/files/crashes/'), upload_to=monitor.models.getUploadPath),
        ),
        migrations.AlterField(
            model_name='issue',
            name='cve',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='etc_numbering',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
