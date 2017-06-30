from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from monitor.models import Issue
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout, views
from django.contrib.auth.models import User

def check_auth(request):
	if not request.user.username:
		raise Http404

def index(request):
	check_auth(request)
	issue_list = Issue.objects.all()
	context = {'issue_list': issue_list, 'userinfo':request.user}
	return render(request, 'track/index.html', context)

def issue_details(request,idx):
	check_auth(request)
	crash_info = None
	try:
		issue = Issue.objects.get(id=idx)
	except ObjectDoesNotExist:
	    raise Http404
	context = {'issue': issue, 'userinfo': request.user}
	return render(request, 'track/detail.html', context)
