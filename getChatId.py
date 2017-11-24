def getId():
    fname = "chatid.txt"
    try:
        f = open(fname, 'r')
    except IOError:
        print "Could not open file: ", fname
        sys.exit()
    CHAT_ID = f.read()
    f.close()
    
    return CHAT_ID

if __name__ == '__main__':
    getId()