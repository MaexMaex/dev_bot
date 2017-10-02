#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telegram
from datetime import datetime
import logging
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from getToken import getToken
from db_handler import DBHandler

#
version = "2.0"
#
startTime = datetime.now()
db = DBHandler()

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))

def checkUser(bot, update):
    user = update.message.from_user
    if db.get_user(user.id) == None:
        return False
    else:
        return True

def start(bot, update):
    user = update.message.from_user
    if db.get_user(user.id) == None:
        update.message.reply_text("Hi " + user.username + ", you've started using d2-bot, you're added to the system. You can now start drinking!")
        db.add_user(user.id, user.username)
    else:
        update.message.reply_text("Howdy, " + user.username + ", you are already registered! For more info typ /help .")

#the stats method returns the statistics of all registered users
def stats(bot, update):
    if checkUser(bot, update):
        stats = db.get_all_statistics()
        update.message.reply_text("These are the statistics for all users!\n")
        for line in stats:
            #update.message.reply_text(user)
            update.message.reply_text(line[0] + " : " + str(line[1]))
    else:
        update.message.reply_text("You haven't signed up to d2-bot, please do so by pressing /start !")
#the status method returns the status of every registered user   
def status(bot, update):
    if checkUser(bot, update):

        status = db.get_all_status()
        update.message.reply_text("The following minotaurs are drinking!\n")
        for user in status:
            update.message.reply_text(user)
    else:
        update.message.reply_text("You haven't signed up to d2-bot, please do so by pressing /start !")
#the bttn method triggers a button switch, updates a users status and increases the users stats
def bttn(bot, update):
    if checkUser(bot, update):
        user = update.message.from_user 
        #check users status
        status = db.get_min_status(user.id) 
        if status[0] == 0:
            db.change_status(user.id, 1)
            #add one to the users stats
            db.add_bttn(user.id)
            update.message.reply_text(user.username + " is drinking!")
        else:
            db.change_status(user.id, 0)
            update.message.reply_text(user.username + " stopped drinking!")
        
    else:
        update.message.reply_text("You haven't signed up to d2-bot, please do so by pressing /start !")
#the getMe method returns the users stats and statistics
def getMe(bot, update):
    if checkUser(bot, update):
        user = update.message.from_user 
        status = db.get_min_status(user.id)
        if status[0] == 0:
            status = "off"
        else:
            status = "on"
        stats = db.get_min_statistics(user.id)
        update.message.reply_text(user.username + " \nstats: " + str(stats[0]) + "\nstatus: " + status)
    else:
        update.message.reply_text("You haven't signed up to d2-bot, please do so by pressing /start !")
#the undo method lets the user undo a bttn
def undo(bot, update):
    if checkUser(bot, update):
        user = update.message.from_user 
        db.remove_bttn(user.id)
        db.change_status(user.id)
        update.message.reply_text("I removed your last bttn and reset your status!")
        getMe(bot, update)
    else:
        update.message.reply_text("You haven't signed up to d2-bot, please do so by pressing /start !")
#the help method displays what this bot is does and give some stats about it
def help(bot, update):
    time = datetime.now() - startTime
    update.message.reply_text("Hi, im d2-bot. Running at stable version " + version + ". \n\nI've been running for " + str(time) + "\n\nRegister yourself with /start \nand then start drinking with /bttn, \nif you make a mistake you can /undo to remove your last bttn. \nHave fun, and remember, you miss 100% of the shots you don't take!")


def main():
    
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    db.setup()
    updater = Updater(token=getToken())
    
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("bttn", bttn))
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("stats", stats))
    dispatcher.add_handler(CommandHandler("status", status))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("undo", undo))
    dispatcher.add_handler(CommandHandler("getMe", getMe))

    dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()