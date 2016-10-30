def getToken():
	#ADD EXCEPTION FOR IF TOKEN DOESN'T EXISTS
	f = open('token.txt', 'r')
	TELEGRAM_TOKEN = f.read()	
	f.close()
	return TELEGRAM_TOKEN