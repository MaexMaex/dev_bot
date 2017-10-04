from db_handler import DBHandler
db = DBHandler()

def main():
    stop = False
    while stop is not True:
        ui()
        userInput = input('> ')

        if userInput == 1:
            
            foundUser = False
            while foundUser is not True:
                username = raw_input('What user do you want to edit: ')
                foundUser = user_check(username)

            id = user_get_id(username)        
            stats_curr = user_stats(id)
            print "with id " + str(id) + " and stats : " + str(stats_curr)
            approved = False
            while approved is not True:
                stats = raw_input('With how much do you want to change (+/-): ')       
                stats = int(stats) + stats_curr
                print username + " stats will change from " + str(stats_curr) + " to " + str(stats)
                cont = raw_input('Ok to continue? (yes/no): ')              
                if cont == "yes":
                    stats_change(id, stats)
                    approved = True

        if userInput == 2:
            users_get_all()
            foundUser = False
            while foundUser is not True:
                username = raw_input('Which user do you want to remove: ')
                foundUser = user_check(username)
            
            id = user_get_id(username)  
            print "with id " + str(id)
            approved = False
            while approved is not True:
                print "Will remove user " + username
                cont = raw_input('Ok to continue? (yes/no): ')
                user_remove(id)
                approved = True

        if userInput == 4:
            print "Closing admin panel"
            stop = True
        
        else:
            pass

def user_stats(id):
    stats = db.get_min_statistics(id)
    return stats[0]

def user_remove(id):    
    db.remove_user(id)
    print "DB wiped user with id " + str(id)

def user_check(username):    
    if db.get_min_id(username) == None:
        print "No user named " + username
        return False
    else:
        print "Found user " + username
        return True

def stats_change(id, stat):
    if db.set_stats_for_min(id, stat) == None:
        print "Changed users stats"
        s = db.get_min_statistics(id)
        print "Now set to " + str(s[0])
    else:
        print "Something is wrong"

def user_get_id(username):
    id = db.get_min_id(username)    
    return id[0]

def users_get_all():
    everyone = db.get_all_statistics()
    for user in everyone:
        print user

def ui():
    print "***********************"
    print "***d2bot admin panel***"
    print "***********************"
    print "What do you want to do?"
    print "***********************"
    print "1: set stats for user"
    print "2: remove user"
    print "3: -"
    print "4: QUIT"

if __name__ == '__main__':
    main()