#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telegram
import logging
import sys
from telegram.error import NetworkError, Unauthorized
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler
from time import sleep
import getToken
import sqlite3

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
#Database for the d2-bot
#Handels all the stats and statuses of the users
#Basic sqlite3 stuff
conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute("""CREATE TABLE minotaurs (
            id integer,
            stats integer,
            status integer
            )""")

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))

def checkUser(bot, update):
    user = update.message.from_user
    if get_user(user.id) == None:
        return False
    else:
        return True


def start(bot, update):
    user = update.message.from_user
    if get_user(user.id) == None:
        update.message.reply_text("Hi " + user.username + ", you've started using d2-bot, your added to the system. You can now start drinking!")
        add_user(user.id)
    else:
        update.message.reply_text("Howdy, " + user.username + ", Im d2-bot running stable version 2.0. Lovely weather today.")

def bttn(bot, update):
    if checkUser:
        user = update.message.from_user
        update.message.reply_text("Huuah")
    else:
        update.message.reply_text("You haven't signed up to d2-bot, please do so by pressing /start !")

#adds a user to the database
def add_user(id):
    with conn:
        c.execute("INSERT INTO minotaurs VALUES (:id, :stats, :status)", {'id': id, 'stats': 0, 'status': 0})

def get_user(id):
    with conn:
        c.execute("SELECT id, stats, status FROM minotaurs WHERE id = :id", {'id': id})
        return c.fetchone()
#adds a bttn for a user with id      
def add_bttn(id):
    with conn:
        c.execute("""UPDATE minotaurs SET stats = stats + 1
                WHERE id = :id""",
                {'id': id})
        change_status(id)
        
#changes the status of a user with id
def change_status(id):
    with conn:
        status = get_min_status(id)
        if status[0] == 1:
            c.execute("""UPDATE minotaurs SET status = :status
                    WHERE id = :id""",
                    {'id': id, 'status': 0})
        else:
            c.execute("""UPDATE minotaurs SET status = :status
                    WHERE id = :id""",
                    {'id': id, 'status': 1})

#get user status with id
def get_min_status(id):
    c.execute("SELECT status FROM minotaurs WHERE id = :id", {'id': id})
    return c.fetchone()
#returns the statistics of the user with id
def get_min_statistics(id):
    c.execute("SELECT stats FROM minotaurs WHERE id = :id", {'id': id})
    return c.fetchone()
#returns a snapshot status of all the users
def get_all_status():
    c.execute("SELECT id, status FROM minotaurs")
    return c.fetchall()
def get_all_statistics():
    c.execute("SELECT id, stats FROM minotaurs")
    return c.fetchall()

#removes a bttn for a user, ONLY used to correct statistics if the user mistakenly double taps
def remove_bttn(id):
    c.execute("""UPDATE minotaurs SET stats = stats - 1
            WHERE id = :id""",
            {'id': id})
#removes a user from the database
def remove_user(id):
    c.execute("DELETE from minotaurs WHERE id = :id", {'id': id})
    pass
def main():
    
    updater = Updater(token=getToken.getToken())
    
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("bttn", bttn))
    dispatcher.add_handler(CommandHandler("start", start))

    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()
    

if __name__ == '__main__':
    main()
    conn.close()