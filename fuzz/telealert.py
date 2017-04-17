import requests
import re
import hashlib

API_KEY = "260965123:AAETYjK6xe5DyjQNhMw6g8HGsmu3n8VVqzo"

URL_BASE = "https://api.telegram.org/bot"+API_KEY
URL_GETME = URL_BASE+"/GetMe"
URL_RECEIVE = URL_BASE+"/getUpdates"
URL_SEND = URL_BASE+"/sendmessage"
URL_SETWEBHOOK = URL_BASE+"/setWebHook"

def send_message(sender_id, target_id, text):
	target_id = str(target_id)
	sender_id = str(sender_id)

	URL_BASE = "https://api.telegram.org/bot"+sender_id
	URL_SEND = URL_BASE+"/sendmessage"

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

