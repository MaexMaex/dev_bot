# -*- coding: utf-8 -*-
import requests
import json
import random 
import datetime

from getToken import getToken
from getApi import getApi

from requests.packages import urllib3
urllib3.disable_warnings()



def getUpdates(offset = None, timeout = 10):

	TELEGRAM_API = getApi()
	TELEGRAM_TOKEN = getToken()

	payload = {}
	payload["timeout"] = timeout		

	if offset:
		payload['offset'] = offset
	try:
		response = requests.get(TELEGRAM_API + "bot" + TELEGRAM_TOKEN + "/getUpdates", params = payload)
		print payload
		print response.text
		ret = json.loads(response.text)
		print ret
		if ['ok']:
			return ret['result']

	except requests.ConnectionError:
		print "Connection error!!!"
		pass
	except ValueError:
		print "Value error"
		pass


if __name__ == '__main__':
	last_id = 0
	while True:
		print "WAITING FOR UPDATES"	
		print last_id
		updates = getUpdates(last_id+1)
			if updates:
				last_id = updates[-1]['update_id']
				for update in updates:
					if '/hello' in update['message']['text']:
						hello(update)
					except KeyError:
						pass
				
