from db_handler import DBHandler
db = DBHandler()

def main():
    stop = False    
    ui()
    while stop is not True:        
        userInput = raw_input('> ')
        if userInput == "1":
            users_get_all()
            

        if userInput == "2":
            users_get_all()
            foundUser = False
            while foundUser is not True:
                username = raw_input('WHICH USER DO YOU WANT TO EDIT: ')
                foundUser = user_check(username)

            id = user_get_id(username)        
            stats_curr = user_stats(id)
            print "WITH ID " + str(id) + " AND STATS : " + str(stats_curr)
            approved = False
            while approved is not True:
                stats = raw_input('CHANGE STATS WITH (+/-): ')       
                stats = int(stats) + stats_curr
                print username + "'s STATS WILL CHANGE FROM " + str(stats_curr) + " TO " + str(stats)
                cont = raw_input('OK TO CONTINUE? (Y/N): ')              
                if cont == "Y":
                    stats_change(id, stats)
                    approved = True
            

        if userInput == "3":
            users_get_all()
            foundUser = False
            while foundUser is not True:
                username = raw_input('WHICH USER DO YOU WANT TO REMOVE: ')
                foundUser = user_check(username)
            
            id = user_get_id(username)  
            print "WITH ID " + str(id)
            approved = False
            while approved is not True:
                print "ARE YOU SURE YOU WANT TO REMOVE " + username
                cont = raw_input('CONTINUE? (Y/N): ')
                if cont == "Y":
                    user_remove(id)
                    approved = True
            )

        if userInput == "4":
            print "CLOSING TERMINAL"
            stop = True
        
        if userInput == "UI":
            ui()

        else:
            pass

def spacing():
    print "\n\n\n"

def user_stats(id):
    stats = db.get_min_statistics(id)
    return stats[0]

def user_remove(id):    
    db.remove_user(id)
    print "REMOVED USER WITH ID " + str(id)

def user_check(username):    
    if db.get_min_id(username) == None:
        print "NO USER NAMED " + username
        return False
    else:
        print "FOUND USER " + username
        return True

def stats_change(id, stat):
    if db.set_stats_for_min(id, stat) == None:
        s = db.get_min_statistics(id)
        print "STATS SET TO " + str(s[0])
    else:
        print "SOMETHING WENT WRONG, PLEASE VERIFY"

def user_get_id(username):
    id = db.get_min_id(username)    
    return id[0]

def users_get_all():
    everyone = db.get_all_statistics()
    
    for user in everyone:
        print user

def ui():
    print "***********************"
    print "*D2-BOT ADMIN TERMINAL*"
    print "***********************"
    print "***WELCOME COMMANDER***"
    print "***********************"
    print "1: PRINT ALL USERS"
    print "2: UPDATE STATS FOR A USER"
    print "3: REMOVE A USER"
    print "4: QUIT"
    print "UI: PRINT THE MENU"

if __name__ == '__main__':
    main()