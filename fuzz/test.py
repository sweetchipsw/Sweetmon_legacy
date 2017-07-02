from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from monitor.models import Machine, Crash, OnetimeToken, AlertInfoUser
from django.http import Http404
import os
import hashlib
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.utils.crypto import get_random_string
from django.conf import settings
from telealert import *


# Send if alert == True
if True:
        userInfo = AlertInfoUser.objects.get(telegram_user="293123771")
        is_alert = True
        if userInfo.use_telegram == False:
                is_alert = False
# If true, get user infromation
if is_alert == True:
        sender = userInfo.telegram_bot_key;
        target = userInfo.telegram_user;
        message = "[New crash detected (From sweetmon)] "
        send_message(sender, target, message);
