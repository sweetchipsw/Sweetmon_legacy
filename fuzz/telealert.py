#!/usr/bin/python3
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

URL_BASE = "https://api.telegram.org/bot"
URL_SEND = "/sendmessage"

def send_with_gmail(serveraddr, port, sender_id, sender_pw, to_addr, body):

	MAIL_SERVER = serveraddr
	MAIL_PORT = port
	SENDER_ID = sender_id
	SENDER_PW = sender_pw

	msg = MIMEMultipart('alternative')
	msg['From'] = "SWEETMON_ALERT"
	msg['To'] = to_addr
	msg['Subject'] = 'New Crash Detected!!'
	msg.attach(MIMEText(body, 'plain', 'utf-8'))

	try:
		server = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
		server.ehlo()
		server.starttls()
		server.login(SENDER_ID, SENDER_PW)
		server.sendmail(msg['From'], to_addr, msg.as_string())
		server.quit()
		return True

	except BaseException as e:
		print("failed to send mail", str(e))
		return False

	return False

def send_message(sender_id, target_id, text):
	result = False

	target_id = str(target_id)
	sender_id = str(sender_id)

	req_url = URL_BASE+sender_id+URL_SEND+"?chat_id="+target_id+"&text="+text
	post = "chat_id="+target_id+"&text="+(text)
	try:
		req_result = requests.get(req_url).json()
		result = req_result['ok']
		if result == True:
			result = True
	except Exception as e:
		return False
	return result
