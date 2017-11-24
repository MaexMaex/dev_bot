#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telegram
from datetime import datetime
import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from getToken import getToken
from db_handler import DBHandler

startTime = datetime.now()
db = DBHandler()

def error(bot, update, error):
    #change the logging level between INFO - normal mode or DEBUG - verbose mode
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)    
    logger.warning('Update "%s" caused error "%s"' % (update, error))

#checkUser checks is the user is already registered for d2-bot, 
#verify that only users from a certain chat have access

def checkUser(bot, update):
    user = update.message.from_user
    chat_id = update.message.chat.id
    print chat_id
    if db.get_user(user.id) == None:
        return False
    else:
        return True

#start registers the user for usage
def start(bot, update):
    user = update.message.from_user
    if db.get_user(user.id) == None:
        if user.username is None:
            update.message.reply_text("You don't seem to have a username set in telegram! Please create one!")
        else:
            update.message.reply_text("Hi " + user.username + ", you've started using d2-bot, you're added to the system. You can now start drinking!")
            db.add_user(user.id, user.username)
    else:
        update.message.reply_text("Howdy, " + user.username + ", you are already registered! For more info typ /help .")

#the stats method returns the statistics of all registered users
def stats(bot, update):
    if checkUser(bot, update):
        stats = db.get_all_statistics()        
        users = "These are the statistics for all users!\n"
        for line in stats:
            users += line[0] + " : " + str(line[1]) + "\n"
        update.message.reply_text(users)
    else:
        update.message.reply_text("You haven't signed up to d2-bot, please do so by pressing /start !")

#the status method returns the status of every registered user   
def status(bot, update):
    if checkUser(bot, update):
        status = db.get_all_status()
        users = "The following minotaurs are drinking!\n"
        for line in status:
            if line[1] == 1:
                users += line[0] + " : " + str(line[1]) + "\n"
            else:
                pass
        update.message.reply_text(users)
    else:
        update.message.reply_text("You haven't signed up to d2-bot, please do so by pressing /start !")

#the bttn method triggers a button switch, updates a users status and increases the users stats
def bttn(bot, update):
    if checkUser(bot, update):
        user = update.message.from_user 
        status = db.get_min_status(user.id) 
        if status[0] == 0:
            db.change_status(user.id, 1)            
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
        update.message.reply_text(user.username + " I removed your last bttn and reset your status!")
        getMe(bot, update)
    else:
        update.message.reply_text("You haven't signed up to d2-bot, please do so by pressing /start !")

#the help method displays what this bot is does and give some stats about it
def help(bot, update):
    time = datetime.now() - startTime
    #################################################################################
    version = "2.2"

    helpGreeting = "Hi, im d2-bot. Running stable version " + version + ".\n\n" \
                + "I've been running for " + str(time) + ".\n\n" \
                + "Register yourself with /start and start drinking with /bttn.\n" \
                + "If you make a mistake you can /undo your last bttn.\n" \
                + "Have fun, and remember, you miss 100% of the shots you don't take!\n" \
                + "Try out the /memes DEMO now, memes will be added in the next update."

    ####################################################################################

    update.message.reply_text(helpGreeting)

#memes displays and created the meme keyboard containing user made memes
def memes(bot, update):
    keyboardlist = ["nalle","h8fk","pope","roope","lisko","jesuis", "hei", "wat", "lettuce", "aliens", "ransu", "rocknroll", "legend"]
    keyboard = []    
    for elem in keyboardlist:
        keyboard.append(InlineKeyboardButton(elem, callback_data=elem))  

    keyboard = [keyboard[x:x+4] for x in range(0, len(keyboard), 4)]   
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

#button represents a button in the meme keyboard, instead of sending a test this method will fetch the meme from the query.data and fetch it from the database
def button(bot, update):
    query = update.callback_query

    bot.edit_message_text(text="/%s" % query.data,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def main():
    db.setup()
    updater = Updater(token=getToken())
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))

    dispatcher.add_handler(CommandHandler("bttn", bttn))
    dispatcher.add_handler(CommandHandler("undo", undo))
    dispatcher.add_handler(CommandHandler("stats", stats))
    dispatcher.add_handler(CommandHandler("status", status))
       
    dispatcher.add_handler(CommandHandler("getMe", getMe))

    dispatcher.add_handler(CommandHandler("memes", memes))
    dispatcher.add_handler(CallbackQueryHandler(button))

    dispatcher.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()