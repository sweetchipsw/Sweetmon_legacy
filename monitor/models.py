from django.db import models
from datetime import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
import os
# Create your models here.

class Machine(models.Model):
	token = models.CharField(max_length=100)
	fuzzer_name = models.CharField(max_length=50)
	target = models.CharField(max_length=200)
	pub_ip = models.CharField(max_length=16)
	pri_ip = models.CharField(max_length=16)
	reg_date = models.DateTimeField(default=datetime.now, blank=True)
	crash = models.IntegerField(default=0)
	testcase = models.IntegerField(default=0)
	ping = models.DateTimeField(blank=True, auto_now=True)

private_storage = FileSystemStorage(location=settings.CRASH_STORAGE_ROOT)

def getUploadPath(instance, filename):
	return '{0}/{1}'.format(instance.crash_file.name, filename)
	
class Crash(models.Model):
	idx = models.AutoField(primary_key=True)
	crash_hash = models.CharField(max_length=100)
	fuzzer_name = models.CharField(max_length=50)
	target = models.CharField(max_length=200)
	reg_date = models.DateTimeField(default=datetime.now, blank=True)
	latest_date = models.DateTimeField(auto_now=True)
	link = models.CharField(max_length=1000)
	title = models.CharField(max_length=1000)
	crashlog = models.CharField(max_length=6553500)
	dup_crash = models.IntegerField(default=0)
	comment = models.CharField(max_length=1000)
	reproducable = models.BooleanField(default=True)
	crash_size = models.IntegerField(default=0)
	crash_file = models.FileField(storage=private_storage, upload_to=getUploadPath)
	isopen = models.BooleanField(default=True)

class Testcase(models.Model):
	idx = models.AutoField(primary_key=True)
	title = models.CharField(max_length=200)
	target = models.CharField(max_length=200)
	description = models.CharField(max_length=1024)
	testcase_url = models.CharField(max_length=1024)
	testcase_size = models.IntegerField(default=0)
	fuzzer_url = models.CharField(max_length=1024, blank=True, null=True)

class Issue(models.Model):
	idx = models.AutoField(primary_key=True)
	title = models.CharField(max_length=200)
	description = models.CharField(max_length=1024)
	link = models.CharField(max_length=1024)
	isopen = models.BooleanField(default=True)
	cve = models.CharField(max_length=200, blank=True, null=True)
	etc_numbering = models.CharField(max_length=200, blank=True, null=True)
	reward = models.IntegerField(default=0)

class AuthInformation(models.Model):
	name = models.CharField(max_length=256)
	password = models.CharField(max_length=256)

class OnetimeToken(models.Model):
	token = models.CharField(max_length=512)
	real_path = models.CharField(max_length=5120)
	is_expired = models.BooleanField(default=False)

class AlertInfoUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	# mail = models.CharField(max_length=512)
	telegram_user = models.CharField(max_length=512)
	telegram_bot_key = models.CharField(max_length=512)
	# use_mail = models.BooleanField(default=False)
	use_telegram = models.BooleanField(default=False)

