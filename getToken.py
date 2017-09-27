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

if __name__ == '__main__':
    getToken()