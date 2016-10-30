# -*- coding: utf-8 -*-
import json
import requests

from getToken import getToken
from getApi import getApi

# FUNCTION FOR SENDING REGULAR MESSAGES
def send(chat_id, msg):
			
	payload = {}
	payload['chat_id'] = chat_id
	payload['text'] = msg
	try:
		response = requests.post(getApi() + "bot" + getToken() + "/sendMessage", params = payload)
		ret  = json.loads(response.text) 
		print 'sendMessage:'
		print response
		print ret
	except ValueError:
		pass
	if ['ok']:
		return True

	return False