# -*- coding: utf-8 -*-
import requests
import json
import random
import datetime
import sys

from requests.packages import urllib3
urllib3.disable_warnings()

def getToken():
    fname = "token.txt"
    try:
        f = open(fname, 'r')
    except IOError:
        print "Could not open file: ", fname
        sys.exit()
    TELEGRAM_TOKEN = f.read()
    f.close()
    return TELEGRAM_TOKEN

def getUpdates(offset=None, timeout=5):

    TELEGRAM_API = "https://api.telegram.org/"
    TELEGRAM_TOKEN = getToken()

    payload = {}
    payload["timeout"] = timeout

    if offset:
        payload['offset'] = offset
    try:
        response = requests.get(TELEGRAM_API + "bot" +
                                TELEGRAM_TOKEN + "/getUpdates", params=payload)

        print payload
        print response.text
        ret = json.loads(response.text)
        print ret
        if ['ok']:
            return ret['result']

    except requests.ConnectionError:
        print "Connection error!!!"
        return None
    except ValueError:
        print "Value error"
        return None

if __name__ == '__main__':
    last_id = 0
    while True:
        print "WAITING FOR UPDATES"
        print last_id
        updates = getUpdates(last_id + 1)

        if updates:
            last_id = updates[-1]['update_id']
            for update in updates:
                try:
                    if '/hello' in update['message']['text']:
                        hello(update)
                except KeyError:
                    pass