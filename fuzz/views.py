from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from monitor.models import Machine, AuthInformation,Crash, OnetimeToken, AlertInfoUser
from django.http import Http404
import os
import hashlib
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.utils.crypto import get_random_string
from django.conf import settings
from telealert import *

# Create your views here.
def check_auth(request):
	if not request.user.username:
		raise Http404

def index(request):
	raise Http404

def register(request):
	if request.method != 'POST':
		raise Http404
	token = ""
	if request.POST.has_key('password') == False:
		raise Http404
	if request.POST.has_key('fuzzer_name') == False:
		raise Http404
	if request.POST.has_key('pri_ip') == False:
		raise Http404
	if request.POST.has_key('pub_ip') == False:
		raise Http404
	if request.POST.has_key('target') == False:
		raise Http404
	password = request.POST['password']
	fuzzer_name = request.POST['fuzzer_name']
	pri_ip = request.POST['pri_ip']
	pub_ip = request.POST['pub_ip']
	target = request.POST['target']

	authinfo = AuthInformation.objects.get(name="sweetfuzz")
	serverpass = authinfo.password
	password = hashlib.sha1("th1s1ss0rt"+password.encode("utf-8")).hexdigest()


	if password != serverpass:
		raise Http404

	token = get_random_string(300)
	token += fuzzer_name
	token += pri_ip
	token += pub_ip
	token += get_random_string(300)
	token = hashlib.sha1(token).hexdigest()

	Machine(token=token, fuzzer_name=fuzzer_name, pub_ip=pub_ip, pri_ip=pri_ip, target=target).save()

	return HttpResponse(str(token))

def ping(request):
	if request.method != 'POST':
		raise Http404
	# ping
	if request.POST.has_key('token') == False:
		raise Http404

	token = request.POST['token']
	fuzzer = Machine.objects.get(token=token)
	fuzzer.ping = datetime.now()
	fuzzer.save()

	return HttpResponse("Done!")

def status(request):
	if request.method != 'POST':
		raise Http404
	# for testcase per min / crash count
	if request.POST.has_key('token') == False:
		raise Http404
	if request.POST.has_key('testcase') == False:
		raise Http404
	if request.POST.has_key('crash') == False:
		raise Http404

	token = request.POST['token']

	testcase = request.POST['testcase']
	crash = request.POST['crash']

	fuzzer = Machine.objects.get(token=token)
	fuzzer.testcase = testcase
	fuzzer.crash = crash
	fuzzer.save()

	return HttpResponse("success")

def crash(request):

	if request.method != 'POST':
		raise Http404
	if request.POST.has_key('token') == False:
		raise Http404
	if request.POST.has_key('crashlog') == False:
		raise Http404
	if request.POST.has_key('title') == False:
		raise Http404

	token = request.POST['token']
	crashlog = request.POST['crashlog']
	title = request.POST['title']

	fuzzer = None
	try:
		fuzzer = Machine.objects.get(token=token)
	except ObjectDoesNotExist:
	    raise Http404

	target = fuzzer.target
	fuzzer_name = fuzzer.fuzzer_name

	crash_hash = hashlib.sha1(title).hexdigest()
	
	Icrash = None
	dup_flag = False

	try:
		Icrash = Crash.objects.get(crash_hash=crash_hash)
		dup_flag = True
	except ObjectDoesNotExist:
		dup_flag = False

	fuzzer.crash = fuzzer.crash + 1
	fuzzer.save()

	if dup_flag == True:
		# we need to save dup crash
		dup_count = Icrash.dup_crash + 1
		Icrash.dup_crash = dup_count

		crashfile = request.FILES['file'] # get 'file' from post

		parent_name = Icrash.crash_file.name
		p_dir = settings.CRASH_STORAGE_ROOT+parent_name.split("/")[0] # get parent crash dir 

		f = open(p_dir+"/"+str(dup_count), "wb") # save new crash into parent's dir (hash/num)
		for chunk in crashfile.chunks():
			f.write(chunk)
		f.close()

		Icrash.save()
		return HttpResponse("success")
	else:
		crashfile = request.FILES['file']
		crashfile.name = hashlib.sha1((crashfile.name+get_random_string(300))).hexdigest()
		crash_size = crashfile.size
		link = crashfile.name
		new_crash = Crash(crash_hash=crash_hash, fuzzer_name=fuzzer_name, target=target, link=link, title=title, crashlog=crashlog, comment="", crash_size=crash_size, crash_file=crashfile)
		new_crash.save()


		# Send if alert == True
		"""
		is_alert = False
		try:
			userInfo = AlertInfoUser.objects.get(telegram_user="293123771")
			is_alert = True
			if userInfo.use_telegram == False:
				is_alert = False
		except ObjectDoesNotExist:
			is_alert = False
		# If true, get user infromation
		if is_alert == True:
			sender = userInfo.telegram_bot_key;
			target = userInfo.telegram_user;
			message = "[New crash detected (From sweetmon)] "
			send_message(sender, target, message);
		"""
		sendswcp("[New crash detected (From sweetmon)] "+title)
	return HttpResponse("success")

def generateToken(request):

	if request.method != 'POST':
		raise Http404
	if request.POST.has_key('idx') == False:
		raise Http404
	if request.POST.has_key('type') == False:
		raise Http404

	check_auth(request)

	error = False
	idx = request.POST['idx']
	file_type = request.POST['type']
	allow_file_types = {"crash":Crash}

	if file_type not in allow_file_types.keys(): # check file types
		raise Http404

	# Get Instanck
	crash = allow_file_types[file_type].objects.get(idx=idx)

	# Get storage path
	storage = crash.crash_file.storage.location

	fname = crash.crash_file.name
	full_path = storage+"/"+fname
	new_token = hashlib.sha256((get_random_string(1024))).hexdigest()

	# Check already exists OTU(One Time Url) by filename.
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
		otf = OnetimeToken(token = new_token, real_path = full_path, is_expired=False)
		otf.save()

	return JsonResponse(result)

def downloadFileByToken(request):
	# Check parameter
	if request.GET.has_key('token') == False:
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

