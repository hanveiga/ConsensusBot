#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
import logging
import data
import bots.meetingsuggestor as ms
from parsing.MessageParser import MessageParser as mp
import parsing.IntentFeedback as gf
from parsing.States import States


from settigns import TOKEN

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

meeting_length = 2
message_stack = []
listening = False
state = States.STARTED
intent_parser = mp()
DATA_FORMAT = '%H:%M %Y-%m-%d'


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start_consensus(bot, update):
    """Cleans/initializes data structures (runs new reasoning)

    :param bot:
    :param update: telegranm.ext.Update
    :return:
    """
    # TODO(scezar): right now requested format is /start_consensus int h
    global message_stack
    message_stack = []
    operated_message = update.message.text
    new_meeting_len = ''
    for letter in operated_message:
        if letter.isdigit():
            new_meeting_len += letter
        elif new_meeting_len:
            global meeting_length
            meeting_length = int(new_meeting_len)
            return

def end_consensus(bot, update):
    """Returns reasoning result (in future it will be running bot queries)

    :param bot:
    :param update: telegranm.ext.Update
    :return:
    """
    times_availability = []
    for message in message_stack:
        for interval in message.list_of_times:
            times_availability.append(interval)

    if ms.get_suggested_meetings(times_availability) == []:
        print "Can't give meeting output yet"
        reply_keyboard = [['Yes', 'No']]
        bot.sendMessage(update.message.chat_id, text="I can't schedule for you yet. Tell me when you are free",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return

    # meeting = ms.get_suggested_meetings(times_availability)[0] # takes highest ranked option
    # a, b = meeting
    # start, end = a
    new_consensus = ms.get_suggested_meetings_topology_sort(message_stack, meeting_length)
    _, start, end, users = new_consensus[0]
    if users == []:
        bot.sendMessage(update.message.chat_id, text="We have a consensus")
        text = 'A date could be between {} and {}'.format(start.strftime(DATA_FORMAT), end.strftime(DATA_FORMAT))
        bot.sendMessage(update.message.chat_id, text=text)

    else:
        for user in users:
            schedule_text = "@"+str(user)
            schedule_text = schedule_text + 'Can you make it between {} and {}'.format(start.strftime(DATA_FORMAT), end.strftime(DATA_FORMAT))
            bot.sendMessage(update.message.chat_id, text= schedule_text)


def times(bot, update):
    """Adds data entities proposed by user

    :param bot:
    :param update: telegranm.ext.Update
    :return:
    """
    if state.value < States.LISTENING.value:
        return
    a = data.DataMessage(update.message.from_user,update.message )
    # add datamessage to a global queue?
    message_stack.append(a)
    print "added time"


def void(bot, update):
    """
    :param bot:
    :param update:
    :return: Nothing. This is to handle irrelevant conversations
    """
    print "Nothing"

process_callback = {

    "start" : start_consensus,
    "end" :   end_consensus,
    "times" : times,
    "None" : void,
}

def intent_extractor(bot, update):
    """
    :param bot:
    :param update:
    :return: Parses the intent and calls the appropriate callback
    """
    intent = intent_parser.extract_intent(update.message.text)
    global state
    feedback, give_reply, state = gf.give_feedback(intent,state)
    if give_reply:
        bot.sendMessage(update.message.chat_id, text=feedback)

    process_callback[intent](bot,update)

def error(bot, update, error):
    logger.warn('Update {} caused error {}'.format(update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Parse text for intent
    dp.add_handler(MessageHandler([Filters.text], intent_extractor))

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler('start_consensus', start_consensus))
    dp.add_handler(CommandHandler('end_consensus', end_consensus))
    dp.add_handler(CommandHandler('times', times))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
