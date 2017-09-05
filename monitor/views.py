from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from monitor.models import Machine, Crash, Testcase, Issue, Profile, DupCrash
from django.http import Http404
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout, views
from django.contrib.auth.models import User
from django.utils.timesince import timesince
from django.template import defaultfilters
import datetime
import glob
import os
import hashlib
import threading

def CheckPostVariable(POST, parameter):
	for param in parameter:
		if param not in POST:
			return False
	return True


def check_auth(request):
	if not request.user.username:
		raise Http404

def index(request):
	check_auth(request)
	machine_count = Machine.objects.filter(owner=request.user).count()
	crash_count = Crash.objects.filter(owner=request.user).count()
	issue_count = Issue.objects.filter(owner=request.user).count()
	cve_count = Issue.objects.filter(owner=request.user).exclude(cve__exact='').count()
	server_count = Machine.objects.filter(owner=request.user).values('pub_ip').distinct().count()
	profiles = Profile.objects.all()
	myprofile = Profile.objects.get(owner=request.user)
	profilenum = profiles.order_by('-id')[0].id

	context = {'server_count':server_count, 'cve_count':cve_count,'issue_count':issue_count, 'crash_count': crash_count, 'machine_count': machine_count, 'userinfo':request.user, 'profilenum':profilenum, 'profile':profiles, 'myprofile':myprofile}
	
	return render(request, 'monitor/index.html', context)

def fuzzer_list(request):
	check_auth(request)
	machine_list = Machine.objects.filter(owner=request.user).order_by('-ping')#.all()#[::-1]#.filter(idx>0).order_by('-idx')
	now = datetime.datetime.now() - datetime.timedelta(minutes=5)
	myprofile = Profile.objects.get(owner=request.user)

	context = {'machine_list': machine_list, 'userinfo':request.user, 'now':now, 'myprofile':myprofile}
	return render(request, 'monitor/fuzzer/list.html', context)

def fuzzer_details(request, idx):
	check_auth(request)
	fuzzer_info = None
	try:
		fuzzer_info = Machine.objects.get(id=idx, owner=request.user)
	except ObjectDoesNotExist:
	    raise Http404
	myprofile = Profile.objects.get(owner=request.user)
	context = {'fuzzer': fuzzer_info, 'userinfo':request.user, 'myprofile':myprofile}
	return render(request, 'monitor/fuzzer/detail.html', context)

def crash_list(request):
	check_auth(request)
	crash_info = Crash.objects.filter(owner=request.user)[::-1]
	myprofile = Profile.objects.get(owner=request.user)
	context = {'crashes': crash_info, 'userinfo':request.user, 'myprofile':myprofile}
	return render(request, 'monitor/crash/list.html', context)

def crash_details(request, idx):
	check_auth(request)
	crash_info = None
	try:
		crash_info = Crash.objects.get(id=idx, owner=request.user)
	except ObjectDoesNotExist:
	    raise Http404
	myprofile = Profile.objects.get(owner=request.user)
	context = {'crash': crash_info, 'userinfo':request.user, 'myprofile':myprofile}
	return render(request, 'monitor/crash/detail.html', context)

def crash_details_dupcrash(request, idx, page=0):
	check_auth(request)
	crash_info = None
	result = {}
	try:

		crash_info = Crash.objects.get(id=idx, owner=request.user)
		Dcrash = DupCrash.objects.filter(owner=request.user, fuzzer=crash_info.fuzzer, original_crash=crash_info)

		result["total"] = len(Dcrash)
		for i in range(0, len(Dcrash)):
			tmp = {}
			tmp["size"] = defaultfilters.filesizeformat(Dcrash[i].crash_file.size)
			tmp["hash"] = Dcrash[i].crash_hash
			tmp["count"] = Dcrash[i].dup_crash
			tmp["reg_date"] = defaultfilters.date(Dcrash[i].reg_date)
			result[i+1] = tmp


		# crash_path = crash_info.crash_file.path.split("/")[:-1]
		# crash_path = "/".join(crash_path)
		# crashes = (glob.glob(crash_path+"/*"))
		# for i in range(0, len(crashes)):
		# 	tmp = {}
		# 	tmp["size"] = os.path.getsize(crashes[i])
		# 	tmp["name"] = os.path.basename(crashes[i])
		# 	tmp["hash"] = hashlib.md5(open(crashes[i],'rb').read()).hexdigest()
		# 	result[i] = tmp
	except ObjectDoesNotExist:
	    raise Http404
	return JsonResponse(result)


def crash_details_modify(request, idx):
	check_auth(request)
	crash_info = None

	parameterList = ['comment']
	if not CheckPostVariable(request.POST, parameterList):
		raise Http404

	try:
		comment = request.POST['comment']
		crash_info = Crash.objects.get(id=idx, owner=request.user)
	except ObjectDoesNotExist:
	    raise Http404

	crash_info.comment = comment
	crash_info.save()
	myprofile = Profile.objects.get(owner=request.user)

	context = {'crash': crash_info, 'userinfo':request.user, 'myprofile':myprofile}
	return render(request, 'monitor/crash/detail.html', context)

def settings_page(request):
	check_auth(request)

	machine_count = Machine.objects.filter(owner=request.user).count()
	crash_count = Crash.objects.filter(owner=request.user).count()
	issue_count = Issue.objects.filter(owner=request.user).count()
	testcase_count = Testcase.objects.filter(owner=request.user).count()
	cve_count = Issue.objects.filter(owner=request.user).exclude(cve__exact='').count()
	server_count = Machine.objects.filter(owner=request.user).values('pub_ip').distinct().count()

	profile = Profile.objects.all()
	myprofile = Profile.objects.get(owner=request.user)
	notification_setting = {'USE_EMAIL_ALERT':settings.USE_EMAIL_ALERT,'USE_TELEGRAM_ALERT':settings.USE_TELEGRAM_ALERT}
	context = {'testcase_count':testcase_count, 'server_count':server_count, 'cve_count':cve_count,'issue_count':issue_count, 'crash_count': crash_count, 'machine_count': machine_count,'userinfo':request.user, 'profiles':profile, 'myprofile':myprofile, 'notification_setting':notification_setting, 'myprofile':myprofile}
	return render(request, 'settings.html', context)






