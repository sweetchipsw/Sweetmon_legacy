from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from monitor.models import Machine, Crash, OnetimeToken, TelegramBot, Profile, DupCrash, AESCipher, getSha256text
from django.http import Http404
import os
import hashlib
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.utils.crypto import get_random_string
from django.conf import settings
from . import telealert

def CheckPostVariable(POST, parameter):
	for param in parameter:
		if param not in POST:
			return False
	return True

# Create your views here.
def check_auth(request):
	if not request.user.username:
		raise Http404

def index(request):
	raise Http404

def register(request):
	if request.method != 'POST':
		raise Http404

	parameterList = ['userkey', 'fuzzer_name', 'pri_ip', 'pub_ip', 'target']
	if not CheckPostVariable(request.POST, parameterList):
		raise Http404

	token = ""
		
	password = request.POST['userkey']
	fuzzer_name = request.POST['fuzzer_name']
	pri_ip = request.POST['pri_ip']
	pub_ip = request.POST['pub_ip']
	target = request.POST['target']

	# Check valid hashkey
	try:
		profile = Profile.objects.get(userkey=password)
	except ObjectDoesNotExist:
	    raise Http404	

	#Generate new hash
	# password = hashlib.sha256((settings.HASHSALT+password)).hexdigest()

	token = get_random_string(300)
	token += fuzzer_name
	token += pri_ip
	token += pub_ip
	token += get_random_string(300)
	token = hashlib.sha1(token.encode('utf-8')).hexdigest()

	Machine(owner=profile.owner, token=token, fuzzer_name=fuzzer_name, pub_ip=pub_ip, pri_ip=pri_ip, target=target).save()

	return HttpResponse(str(token))

def ping(request):
	if request.method != 'POST':
		raise Http404

	parameterList = ['token']
	if not CheckPostVariable(request.POST, parameterList):
		raise Http404

	token = request.POST['token']
	fuzzer = Machine.objects.get(token=token)
	fuzzer.ping = datetime.now()
	fuzzer.save()

	return HttpResponse("Done!")

def status(request):
	if request.method != 'POST':
		raise Http404

	parameterList = ['token', 'testcase', 'crash']
	if not CheckPostVariable(request.POST, parameterList):
		raise Http404

	token = request.POST['token']
	testcase = request.POST['testcase']
	crash = request.POST['crash']

	fuzzer = Machine.objects.get(token=token)
	fuzzer.testcase = testcase
	fuzzer.crash = crash
	fuzzer.save()

	return HttpResponse("success")

def generateToken(request):

	if request.method != 'POST':
		raise Http404

	check_auth(request)

	parameterList = ['idx', 'type']
	if not CheckPostVariable(request.POST, parameterList):
		raise Http404

	# print("hit")


	error = False
	idx = request.POST['idx']
	file_type = request.POST['type']
	allow_file_types = {"crash":Crash, "dup_crash":DupCrash}

	if file_type not in allow_file_types.keys(): # check file types
		raise Http404

	try:
		crash = Crash.objects.get(id=idx)
		if file_type == "dup_crash":
			crash_hash = request.POST['crash_hash']
			crash = allow_file_types[file_type].objects.get(owner=request.user, original_crash=crash, crash_hash=crash_hash)
	except:
		raise Http404

	# Check owner
	# print(crash.owner != request.user)
	if crash.owner != request.user:
		raise Http404

	# Get storage path
	storage = crash.crash_file.storage.location

	fname = crash.crash_file.name

	full_path = storage + "/" + fname
	if file_type == "dup_crash":
		full_path = fname
	new_token = hashlib.sha256((get_random_string(1024).encode('utf-8'))).hexdigest()

	# Check if already exists OTU(One Time Url) by filename.
	# It prevents generating duplcated URL
	try:
		otu = OnetimeToken.objects.get(real_path=full_path, is_expired=False)
		# Set error flag when exists duplicated request.
		error = True
	except ObjectDoesNotExist:
		# pass if not exists.
	    pass

	current_uri = request.build_absolute_uri().replace(request.get_full_path(), "")

	result = {}
	if error:
		result['token'] = otu.token
		result['url'] = current_uri+"/fuzz/download?token="+otu.token
		result['dup'] = True
	else:
		result['token'] = new_token
		result['url'] = current_uri+"/fuzz/download?token="+new_token
		result['dup'] = False
		otf = OnetimeToken(owner=request.user, token=new_token, real_path=full_path, is_expired=False)
		otf.save()

	return JsonResponse(result)

def downloadFileByToken(request):
	# Check parameter
	parameterList = ['token']
	if not CheckPostVariable(request.GET, parameterList):
		raise Http404
	# Get 'token' parameter
	token = request.GET['token']

	# Check if exists OTT by token
	try:
		otf = OnetimeToken.objects.get(token=token)
	except ObjectDoesNotExist:
	    raise Http404

	# Check expire
	if otf.is_expired == True:
		raise Http404

	f = open(otf.real_path, "rb")
	mimetype = "application/octet-stream"
	response = HttpResponse(f.read(), content_type=mimetype)
	response["Content-Disposition"] = "attachment; filename="+otf.real_path.split("/")[-1]

	otf.is_expired = True
	otf.save()
	f.close()

	return response 

def SendMsgViaTelegramByUid(profile, message):

	result = False
	if profile.use_telegram_alert == False or settings.USE_TELEGRAM_ALERT == False:
		return False
	# API Key of telegram bot
	try:
		apikey = profile.telegram.telegram_bot_key;
		target = profile.telegram_chatid;
	except AttributeError as e:
		return False

	if apikey == "" or target == "" or message == "":
		return False

	result = telealert.send_message(apikey, target, message)

	return result


def SendMsgViaEmailByUid(profile, message):
	result = False

	target_email = profile.email;
	email = profile.emailbot
	if email == "" or message == "":
		return False
	server = email.smtp_server
	port = email.smtp_port
	sender_id = email.email_id
	sender_pw = email.email_pw_enc

	aeskey = getSha256text((email.owner.username + settings.SECRET_KEY + email.owner.username).encode('utf-8'))[:32]

	sender_pw = AESCipher(aeskey).decrypt(sender_pw)
	try:
		result = telealert.send_with_gmail(server, port, sender_id, sender_pw, target_email, message)
	except Exception as e:
		result = False
	return result

def alert(request, test=False):
	if request.method != 'POST':
		raise Http404

	check_auth(request)

	result = False

	parameterList = ['message', 'via']
	if not CheckPostVariable(request.POST, parameterList):
		raise Http404

	message = request.POST['message']
	error = None
	if test == True:
		message = "This is test message."
	via = request.POST['via']

	if via == "telegram":
		try:
			profile = Profile.objects.get(owner=request.user)
		except ObjectDoesNotExist:
			raise Http404

		result = SendMsgViaTelegramByUid(profile, message)
		if result == False:
			error = "Please check your telegram settings."
	elif via == "email":
		try:
			profile = Profile.objects.get(owner=request.user)
		except ObjectDoesNotExist:
			return False

		if profile.use_email_alert == False or settings.USE_EMAIL_ALERT == False:
			return False

		email = profile.emailbot
		target_email = profile.email

		result = SendMsgViaEmailByUid(profile, message)

		if result == False:
			error = "Please check your email settings."
	return JsonResponse({"result":result, "error":error})

def alert_test(request):
	return alert(request, test=True)


def crash(request):
	# Check POST
	if request.method != 'POST':
		raise Http404

	# Check Parameter
	parameterList = ['token', 'crashlog', 'title']
	if not CheckPostVariable(request.POST, parameterList):
		raise Http404

	# Get Parameters
	token = request.POST['token']
	crashlog = request.POST['crashlog']
	title = request.POST['title']

	# Get fuzzer information by token
	fuzzer = None
	try:
		fuzzer = Machine.objects.get(token=token)
	except ObjectDoesNotExist:
		raise Http404

	target = fuzzer.target
	fuzzer_name = fuzzer.fuzzer_name

	# Generate hash by title
	crash_hash = hashlib.sha1(title.encode("utf-8")).hexdigest()

	# Check if crash already exists
	Icrash = None
	dup_flag = False

	try:
		Icrash = Crash.objects.get(crash_hash=crash_hash)
		dup_flag = True
	except ObjectDoesNotExist:
		dup_flag = False

	# Add 1 to crash count.
	fuzzer.crash_count = fuzzer.crash_count + 1
	fuzzer.save()

	if dup_flag == True:
		# If duplicate crash
		# we need to save dup crash
		dup_count = Icrash.dup_crash + 1
		Icrash.dup_crash = dup_count

		crashfile = request.FILES['file']  # get 'file' from post

		parent_name = Icrash.crash_file.name
		p_dir = settings.CRASH_STORAGE_ROOT + parent_name.split("/")[0]  # get parent crash dir

		file_hash = hashlib.md5(crashfile.read()).hexdigest()

		try:
			Dcrash = DupCrash.objects.get(crash_hash=file_hash)
			Dcrash.dup_crash = Dcrash.dup_crash + 1;
			Dcrash.save()
		except ObjectDoesNotExist:
			new_dup_crash = DupCrash(owner=fuzzer.owner, fuzzer=fuzzer, original_crash=Icrash, crash_hash=file_hash,
			                         crash_file=p_dir + "/" + str(dup_count))

			# Save crash name as 1, 2, 3, ...
			f = open(p_dir + "/" + str(dup_count), "wb")  # save new crash into parent's dir (hash/num)
			for chunk in crashfile.chunks():
				f.write(chunk)
			f.close()

			new_dup_crash.save()
		Icrash.save()
		return HttpResponse("success")
	else:
		# If new crash
		crashfile = request.FILES['file']
		crashfile.name = hashlib.sha1((crashfile.name + get_random_string(300)).encode("utf-8")).hexdigest()
		# crash_size = crashfile.size
		link = crashfile.name
		new_crash = Crash(owner=fuzzer.owner, fuzzer=fuzzer, crash_hash=crash_hash, title=title, crashlog=crashlog,
		                  crash_file=crashfile)
		new_crash.save()

		# Alert
		profile = None
		try:
			profile = Profile.objects.get(owner=fuzzer.owner)
		except ObjectDoesNotExist:
			raise Http404

		message = "This is test message"


		if profile.use_telegram_alert == True:
			# Send msg via telegram
			SendMsgViaTelegramByUid(profile, message)

		if profile.use_email_alert == True:
			# Send msg via email
			SendMsgViaEmailByUid(profile, message)

		# sendswcp("[New crash detected (From sweetmon)] "+title)
	return HttpResponse("success")  # Return success



