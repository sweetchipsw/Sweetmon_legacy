# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('monitor', '0011_onetimetoken_is_expired'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlertInfoUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('telegram_user', models.CharField(max_length=512)),
                ('telegram_bot_key', models.CharField(max_length=512)),
                ('use_telegram', models.BooleanField(default=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
