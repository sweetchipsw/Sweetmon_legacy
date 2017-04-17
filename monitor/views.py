from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from monitor.models import Machine, Crash, Testcase, Issue
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout, views
from django.contrib.auth.models import User
import datetime

def check_auth(request):
	if not request.user.username:
		raise Http404

def index(request):
	check_auth(request)
	machine_count = Machine.objects.all().count()
	crash_count = Crash.objects.all().count()
	issue_count = Issue.objects.all().count()
	cve_count = Issue.objects.exclude(cve__exact='').count()
	server_count = Machine.objects.values('pub_ip').distinct().count()

	context = {'server_count':server_count, 'cve_count':cve_count,'issue_count':issue_count, 'crash_count': crash_count, 'machine_count': machine_count, 'userinfo':request.user}
	
	return render(request, 'monitor/index.html', context)

def fuzzer_list(request):
	check_auth(request)
	machine_list = Machine.objects.filter(testcase=0).order_by('-ping')#.all()#[::-1]#.filter(idx>0).order_by('-idx')
	now = datetime.datetime.now() - datetime.timedelta(minutes=5)
	context = {'machine_list': machine_list, 'userinfo':request.user, 'now':now}
	return render(request, 'monitor/fuzzer/list.html', context)

def fuzzer_details(request, idx):
	check_auth(request)
	fuzzer_info = None
	try:
		fuzzer_info = Machine.objects.get(id=idx)
	except ObjectDoesNotExist:
	    raise Http404
	context = {'fuzzer': fuzzer_info, 'userinfo':request.user}
	return render(request, 'monitor/fuzzer/detail.html', context)

def crash_list(request):
	check_auth(request)
	crash_info = Crash.objects.all()[::-1]
	context = {'crashes': crash_info, 'userinfo':request.user}
	return render(request, 'monitor/crash/list.html', context)

def crash_details(request, idx):
	check_auth(request)
	crash_info = None
	try:
		crash_info = Crash.objects.get(idx=idx)
	except ObjectDoesNotExist:
	    raise Http404
	context = {'crash': crash_info, 'userinfo':request.user}
	return render(request, 'monitor/crash/detail.html', context)

def crash_details_modify(request, idx):
	check_auth(request)
	crash_info = None
	# if request.POST.has_key('comment') == False:
	# 	raise Http404
	try:
		crash_info = Crash.objects.get(idx=idx)
	except ObjectDoesNotExist:
	    raise Http404
	context = {'crash': crash_info, 'userinfo':request.user}
	return render(request, 'monitor/crash/detail.html', context)