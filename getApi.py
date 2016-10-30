def getApi():
	#ADD EXCEPTION FOR IF TOKEN DOESN'T EXISTS
	f = open('api.txt', 'r')
	TELEGRAM_API = f.read()	
	f.close()
	return TELEGRAM_API