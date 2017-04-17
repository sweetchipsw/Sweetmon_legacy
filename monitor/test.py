from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from telealert import *
from monitor.models import *
me = 293123771

send_message(me, "test")
