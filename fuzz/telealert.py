import requests
import re
import hashlib
import os
from django.conf import settings

# TELEBOT_APIKEY = "260965123:AAETYjK6xe5DyjQNhMw6g8HGsmu3n8VVqzo"
API_KEY = settings.TELEBOT_APIKEY

URL_BASE = "https://api.telegram.org/bot"+API_KEY
URL_GETME = URL_BASE+"/GetMe"
URL_RECEIVE = URL_BASE+"/getUpdates"
URL_SEND = URL_BASE+"/sendmessage"
URL_SETWEBHOOK = URL_BASE+"/setWebHook"

def GenerateKey(len):
	rd = os.urandom(len).encode("hex")
	return rd[:(len/2)]

def ParseKey(result):
	user_infos = []
	user_info = {"userName":"", "userId":"", "secretKey":"", "submitKey":""}
	for msg in result["result"]:

		userId = msg["message"]["chat"]["id"]
		userName = msg["message"]["chat"]["username"]
		userMsg = msg["message"]["text"]

		user_info["userName"] = userName
		user_info["userId"] = userId
		user_info["submitKey"] = userMsg

		user_infos.append(user_info)

	return user_info

def UpdateSecretKey():
	req_url = URL_RECEIVE
	try:
		result = requests.get(req_url).json()
		result = ParseKey(result)
	except Exception as e:
		return False
	return result

def send_message(sender_id, target_id, text):
	target_id = str(target_id)
	sender_id = str(sender_id)

	req_url = URL_SEND+"?chat_id="+target_id+"&text="+text
	post = "chat_id="+target_id+"&text="+(text)
	try:
		result = requests.get(req_url).json()
		result = result['ok']
	except Exception, e:
		return False
	return result


def sendswcp(message):
	send_message(API_KEY, "293123771", message)

print(UpdateSecretKey())