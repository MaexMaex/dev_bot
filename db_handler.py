#Database for the d2-bot
#Handels all the stats and statuses of the users
#Basic sqlite3 stuff
import sqlite3

#conn = sqlite3.connect(':memory:')

#c.execute("""CREATE TABLE minotaurs (
#            id integer,
#            stats integer,
#            status integer
#            )""")

class DBHandler:

    def __init__(self, dbname="minotaurs.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)
        self.c = self.conn.cursor()

    def setup(self):
        with self.conn:
            self.c.execute("""CREATE TABLE IF NOT EXISTS minotaurs (id integer, name text, stats integer, status integer)""")

    #adds a user to the database
    def add_user(self, id, name):
        with self.conn:
            self.c.execute("INSERT INTO minotaurs VALUES (:id, :name, :stats, :status)", {'id': id, 'name': name, 'stats': 0, 'status': 0})
    
    #fetches user with id
    def get_user(self, id):
        with self.conn:
            self.c.execute("SELECT id, name, stats, status FROM minotaurs WHERE id = :id", {'id': id})
            return self.c.fetchone()

    #adds a bttn for a user with id      
    def add_bttn(self, id):
        with self.conn:
            self.c.execute("""UPDATE minotaurs SET stats = stats + 1
                    WHERE id = :id""",
                    {'id': id})
            
    #changes the status of a user with id
    def change_status(self, id, status):
        with self.conn:
            self.c.execute("""UPDATE minotaurs SET status = :status
                    WHERE id = :id""",
                    {'id': id, 'status': status})

    #get user status with id
    def get_min_status(self, id):
        self.c.execute("SELECT status FROM minotaurs WHERE id = :id", {'id': id})
        return self.c.fetchone()

    #returns the statistics of the user with id
    def get_min_statistics(self, id):
        self.c.execute("SELECT stats FROM minotaurs WHERE id = :id", {'id': id})
        return self.c.fetchone()

    #returns a snapshot status of all the users
    def get_all_status(self):
        self.c.execute("SELECT name, status FROM minotaurs")
        return self.c.fetchall()

    #returns the statistics for all users in the database
    def get_all_statistics(self):
        self.c.execute("SELECT name, stats FROM minotaurs ORDER BY stats DESC")
        return self.c.fetchall()

    #removes a bttn for a user, ONLY used to correct statistics if the user mistakenly double taps
    def remove_bttn(self, id):
        self.c.execute("""UPDATE minotaurs SET stats = stats - 1
                WHERE id = :id""",
                {'id': id})
    
    #sets a stat for a user, only used if there has been a bot downtime
    def set_stats_for_min(self, id, stats):
        self.c.execute("""UPDATE minotaurs SET stats = :stats
                WHERE id = :id""",
                {'id': id, 'stats': stats})        

    #removes a user from the database
    #def remove_user(self, id):
    #    self.c.execute("DELETE from minotaurs WHERE id = :id", {'id': id})
        
    
    