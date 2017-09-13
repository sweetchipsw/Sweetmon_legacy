from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from monitor.models import Profile
from track.models import Issue
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout, views
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
	issue_list = Issue.objects.filter(owner=request.user)
	myprofile = Profile.objects.get(owner=request.user)
	context = {'issue_list': issue_list, 'userinfo':request.user, "myprofile":myprofile}

	return render(request, 'track/index.html', context)

@login_required
def issue_details(request,idx):
	crash_info = None
	try:
		issue = Issue.objects.get(id=idx)
	except ObjectDoesNotExist:
	    raise Http404
	myprofile = Profile.objects.get(owner=request.user)
	context = {'issue': issue, 'userinfo': request.user, "myprofile":myprofile}
	return render(request, 'track/detail.html', context)
