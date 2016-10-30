from send import send
def hello(update):
	message = update['message']
	theId = message['chat']['id']
	user = message['from']
	User_Frst = user['first_name']
	message = "Hello %s! "
	send(theId, message)