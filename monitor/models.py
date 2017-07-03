from django.db import models
from datetime import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from django.db.models.signals import pre_save, post_save
import hashlib
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, User
import binascii

###############################################################################
# Storage
###############################################################################
private_storage = FileSystemStorage(location=settings.CRASH_STORAGE_ROOT)
fuzzerStorage = FileSystemStorage(location=settings.FUZZER_STORAGE_ROOT)
testcaseStorage = FileSystemStorage(location=settings.TESTCASE_STORAGE_ROOT)
userimageStorage = FileSystemStorage(location=settings.USERIMAGE_STORAGE_ROOT)

def getSha256text(plain):
	h = hashlib.sha256(plain).hexdigest()
	return h


def getUploadPath(instance, filename):
	return '{0}/{1}'.format(instance.crash_file.name, filename)

def getimageUploadPath(instance, filename):
	return '{0}.jpg'.format( getSha256text(str(os.urandom(32)).encode('utf-8')) )

# Fuzzing machine model
class Machine(models.Model):
	fuzzer_name = models.CharField(max_length=50)
	target = models.CharField(max_length=200)
	owner = models.ForeignKey(User, default=1)
	crash = models.IntegerField(default=0)
	testcase = models.IntegerField(default=0)
	ping = models.DateTimeField(blank=True, auto_now=True)
	reg_date = models.DateTimeField(default=datetime.now, blank=True)
	#regist_date = models.DateTimeField(default=datetime.now, blank=True)
	pub_ip = models.CharField(max_length=16)
	#public_ip = models.CharField(max_length=16)
	pri_ip = models.CharField(max_length=16)
	#private_ip = models.CharField(max_length=16)
	token = models.CharField(max_length=100)

	def __str__(obj):
		return "%s" % (obj.fuzzer_name)


class Crash(models.Model):
	title = models.CharField(max_length=1000)
	target = models.CharField(max_length=200)
	fuzzer_name = models.CharField(max_length=50)
	crash_hash = models.CharField(max_length=100)
	link = models.CharField(max_length=1000)
	crashlog = models.CharField(max_length=6553500)
	dup_crash = models.IntegerField(default=0)
	reproducable = models.BooleanField(default=True)
	crash_file = models.FileField(storage=private_storage, upload_to=getUploadPath)
	reg_date = models.DateTimeField(default=datetime.now, blank=True) # first date
	latest_date = models.DateTimeField(auto_now=True)
	comment = models.CharField(max_length=100000)
	owner = models.ForeignKey(User)
	is_encrypted = models.BooleanField(default=False)

	# DEPRECATED
	#isopen = models.BooleanField(default=True) # Deprecated
	#crash_size = models.IntegerField(default=0) # Deprecated

	def __str__(obj):
		return "%s" % (obj.title)


class Testcase(models.Model):
	title = models.CharField(max_length=200)
	fuzzerName = models.CharField(max_length=200)
	binaryName = models.CharField(max_length=200)
	target = models.CharField(max_length=200)
	description = models.TextField(max_length=1024)
	testcase_url = models.CharField(max_length=1024)
	fuzzer_url = models.CharField(max_length=1024, blank=True, null=True)
	fuzzerFile = models.FileField(storage=fuzzerStorage, blank=True)
	testcaseFile = models.FileField(storage=testcaseStorage, blank=True)
	owner = models.ForeignKey(User)

	# DEPRECATED
	#testcase_size = models.IntegerField(default=0) # Deprecated

	def __str__(obj):
		return "%s" % (obj.title)


class Issue(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField(max_length=1024)
	link = models.CharField(max_length=1024)
	isopen = models.BooleanField(default=True)
	cve = models.CharField(max_length=200, blank=True, null=True)
	etc_numbering = models.CharField(max_length=200, blank=True, null=True)
	reward = models.IntegerField(default=0)
	owner = models.ForeignKey(User)

	def __str__(obj):
		return "%s" % (obj.title)


# class AuthInformation(models.Model):
# 	name = models.CharField(max_length=256)
# 	password = models.CharField(max_length=256)
# 	do_hash = models.BooleanField(default=True)
# 	owner = models.ForeignKey(User)

# 	def __str__(obj):
# 		return "%s" % (obj.name)


class OnetimeToken(models.Model):
	token = models.CharField(max_length=512)
	real_path = models.CharField(max_length=5120)
	is_expired = models.BooleanField(default=False)
	owner = models.ForeignKey(User)


class TelegramBot(models.Model):
	telegram_bot_name = models.CharField(max_length=512)
	telegram_bot_key = models.CharField(max_length=512)
	is_activated = models.BooleanField(default=False)
	is_public = models.BooleanField(default=False, help_text="Note That, other user can modify/delete this configuration.")
	owner = models.ForeignKey(User)

	def __str__(obj):
		return "%s" % (obj.telegram_bot_name)

# Profile to manage account
class Profile(models.Model):
	owner = models.ForeignKey(User)

	##
	last_name = models.CharField(max_length=512, null=True, blank=True)
	first_name = models.CharField(max_length=512, null=True, blank=True)
	email = models.EmailField(max_length=512, null=True, blank=True)
	test_email = models.BooleanField(default=False, help_text="Please check if you want to test email alert.")
	telegram_chatid = models.CharField(max_length=12,null=True, blank=True, help_text="To get your chat_id, Add '@get_id_bot' and send '/my_id'")
	test_telegram = models.BooleanField(default=False, help_text="Please check if you want to test telegram alert.")
	##

	profile_image = models.FileField(storage=userimageStorage, null=True, blank=True, upload_to=getimageUploadPath)
	userkey = models.TextField(null=True, blank=True)
	telegram = models.ForeignKey(TelegramBot, null=True, blank=True)
	public_key = models.TextField(max_length=10000, blank=True, null=True)
	use_telegram_alert = models.BooleanField(default=False, help_text="You should fill out telegram_chatid to use this feature.")
	use_email_alert = models.BooleanField(default=False, help_text="You should fill out email of your profile to use this feature.")
	# use_encryption = models.BooleanField(default=False, help_text="DEPRECATED FEATURE")

	def __str__(obj):
		return "%s" % (obj.owner)



def problem_hash_check_pre_save(sender, **kwargs):
	obj = kwargs.get('instance', None)
	obj.password = getSha256text("th1s1ss0rt"+obj.password)

def create_profile(sender, **kwargs):
	# Gen userkey
	userkey = getSha256text( str(os.urandom(32)).encode('utf-8') )
	user = kwargs["instance"]
	# print(kwargs, userkey, user)
	if kwargs["created"]:
		# Create user
		user_profile = Profile(owner=user, userkey=userkey)
		user_profile.email = user.email
		user_profile.last_name = user.last_name
		user_profile.first_name = user.first_name
		user_profile.save()

		# Allow access to admin page
		user = User.objects.get(id=user.id)
		user.is_staff = True;
		user.save()

		# print("created")
	# print("hit")

def SyncUserProfile(sender, **kwargs):
	# Gen userkey
	profile = kwargs["instance"]
	# print(kwargs)
	if not kwargs["created"]:
		# Create user
		print(profile.owner.id)
		user_profile = User.objects.get(id=profile.owner.id)
		user_profile.email = profile.email
		user_profile.last_name = profile.last_name
		user_profile.first_name = profile.first_name
		user_profile.save()
		# print("modified")
	# print("hit sync")

post_save.connect(create_profile, sender=User)
post_save.connect(SyncUserProfile, sender=Profile)
# pre_save.connect(problem_hash_check_pre_save, sender=AuthInformation)

