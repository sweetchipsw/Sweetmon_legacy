from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from monitor.models import Testcase, Profile
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout, views
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
	testcase_list = Testcase.objects.filter(owner=request.user)
	myprofile = Profile.objects.get(owner=request.user)

	context = {'testcase_list': testcase_list, 'userinfo':request.user, 'myprofile':myprofile}
	return render(request, 'testcase/index.html', context)

@login_required
def testcase_details(request,idx):
	crash_info = None
	try:
		testcase = Testcase.objects.get(id=idx)
	except ObjectDoesNotExist:
	    raise Http404
	myprofile = Profile.objects.get(owner=request.user)
	context = {'testcase': testcase, 'userinfo':request.user, 'myprofile':myprofile}
	return render(request, 'testcase/detail.html', context)
