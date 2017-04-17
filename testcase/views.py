from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from monitor.models import Testcase
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout, views
from django.contrib.auth.models import User

def check_auth(request):
	if not request.user.username:
		raise Http404

def index(request):
	check_auth(request)
	testcase_list = Testcase.objects.all()
	context = {'testcase_list': testcase_list, 'userinfo':request.user}
	return render(request, 'testcase/index.html', context)

def testcase_details(request,idx):
	check_auth(request)
	crash_info = None
	try:
		testcase = Testcase.objects.get(idx=idx)
	except ObjectDoesNotExist:
	    raise Http404
	context = {'testcase': testcase, 'userinfo':request.user}
	return render(request, 'testcase/detail.html', context)
