import requests
import json
import random 
import datetime

#TELEGRAM_TOKEN = "INSERT YOUR TOKEN HERE"
TELEGRAM_API = "https://api.telegram.org/"

from requests.packages import urllib3
urllib3.disable_warnings()

class Bot(object):


	"""docstring for Bot"""
	def __init__(self, arg):
		super(Bot, self).__init__()
		self.arg = arg
	def getUpdates(offset = None, timeout = 10):

		payload = {}
		payload["timeout"] = timeout		

	if offset:
		payload['offset'] = offset
	try:
		response = requests.get(TELEGRAM_API)
	except Exception as e:
		raise
	else:
		pass
	finally:
		pass


if __name__ == '__main__':
	main()