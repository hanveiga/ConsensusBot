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
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup
import logging
import data
import bots.meetingsuggestor as ms
from parsing.MessageParser import MessageParser as mp
import parsing.IntentFeedback as gf
from parsing.States import *
from collections import defaultdict
from bots.meetingsuggestor import ResultObject
import doodle.export_doodle as doodle


from settigns import TOKEN

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

meeting_length = 2
message_stack = []
intent_parser = mp()
state = States.STARTED
HOUR_FORMAT = '%H:%M'
DATA_FORMAT = '%A, %d. %B'
DATE_FORMAT = '%H:%M %d/%m'
users_dict_id_to_username = {}
users_to_query = []
scheduling_policies = []

def restart():
    global message_stack, users_dict_id_to_username, users_to_query, scheduling_policies, state
    message_stack = []
    state = States.STARTED
    users_dict_id_to_username = {}
    users_to_query = []
    scheduling_policies = []
    print "Restarting bot..."

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
    global state
    global users_to_query
    global scheduling_policies

    if state.value >= States.FINALIZING.value:
        return

    if state.value < States.LISTENING.value or not message_stack:
        print "Can't give meeting output yet"
        bot.sendMessage(update.message.chat_id, text="I can't schedule for you yet. Tell me when you are free")
        state = States.LISTENING
        return

    times_availability = []
    for message in message_stack:
        for interval in message.list_of_times:
            times_availability.append(interval)

    new_consensus = ms.get_suggested_meetings_topology_sort(message_stack, meeting_length)
    if new_consensus == []:
        bot.sendMessage(update.message.chat_id, text="I couldn't find a spot. Keep talking to me!")
        return



    # meeting = ms.get_suggested_meetings(times_availability)[0] # takes highest ranked option
    # a, b = meeting
    # start, end = a
    new_consensus = ms.get_suggested_meetings_topology_sort(message_stack, meeting_length)

    scheduling_policies = new_consensus[:]

    start = new_consensus[0].date_from
    end = new_consensus[0].date_to
    users = new_consensus[0].users_to_ask
    reply_keyboard = [['Yes', 'No', 'You guys go on!']]

    if not users:

        bot.sendMessage(update.message.chat_id, text="We have a consensus.")
        string = 'The final schedule is between ' #{} and {} on {}'
        text = get_text(string,start,end)
        bot.sendMessage(update.message.chat_id, text=text)
        restart()

        # for user in users_dict_id_to_username.keys():
        #     if users_dict_id_to_username[user].username is not "":
        #         user_handle = users_dict_id_to_username[user].username
        #     else:
        #         user_handle = str(user) + " (" + users_dict_id_to_username[user].first_name + ")"
        #     schedule_text = "@" + user_handle
        #     schedule_text = schedule_text + ' can you make it then?'
        #         # .format(
        #         # start.strftime(HOUR_FORMAT),
        #         # start.strftime(DATA_FORMAT),
        #         # end.strftime(HOUR_FORMAT),
        #         # end.strftime(DATA_FORMAT))
        #     bot.sendMessage(update.message.chat_id, text= schedule_text,
        #                     reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard = True,
        #                                                     one_time_keyboard=False,selective=True))
        # scheduling_policies = []
        # final_schedule = ResultObject(0,start,end,users_dict_id_to_username.keys())
        # users_to_query = users_dict_id_to_username.keys()
        # scheduling_policies = [final_schedule]
        # state = States.FINALIZING

    else:

        state = States.FINALIZING

        users_to_query = users[:]

        for user in users:
            global users_dict_id_to_username

            if users_dict_id_to_username[user].username is not "":
                user_handle = users_dict_id_to_username[user].username
            else:
                user_handle = str(user) + " (" + users_dict_id_to_username[user].first_name + ")"

            schedule_text = "@" + user_handle
            schedule_text = schedule_text + get_text(' can you make it ', start, end) + '?'

            bot.sendMessage(update.message.chat_id, text= schedule_text,
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard = True,
                                                            one_time_keyboard=True,selective=True))


def times(bot, update):
    """Adds data entities proposed by user

    :param bot:
    :param update: telegranm.ext.Update
    :return:
    """
    if state.value < States.LISTENING.value:
        return

    message_stack.append(data.DataMessage(update.message.from_user, update.message))
    user = update.message.from_user
    global users_dict_id_to_username
    if user.id not in users_dict_id_to_username:
        users_dict_id_to_username[user.id] = user
    print "added time"


def export(bot,update):

    """Adds data entities proposed by user

    :param bot:
    :param update: telegranm.ext.Update
    :return:
    """
    all_users = []
    for user in message_stack:
        if user.user in all_users:
            pass
        else:
            all_users.append(user.user)

    all_options_text = []
    preferences = defaultdict(list)
    full_preferences = defaultdict(list)
    if message_stack == []:
        bot.sendMessage(update.message.chat_id, text='There are no entries to export.')
        return
    else:
        new_consensus = ms.get_suggested_meetings_topology_sort(message_stack, meeting_length)
        for result in new_consensus:
            print result.date_from
            print result.date_to
            print result.users_to_ask
            all_options_text.append({'text':result.date_from.strftime(DATE_FORMAT)+'-'+result.date_to.strftime(DATE_FORMAT)})
            for user in all_users:
                if user in result.users_to_ask:
                    full_preferences[users_dict_id_to_username[user].first_name].append(0)
                else:
                    full_preferences[users_dict_id_to_username[user].first_name].append(1)
                # positive
    url = doodle.generate_doodle(full_preferences,all_options_text)
    bot.sendMessage(update.message.chat_id, text='Doodle created, follow link: '+url)



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

def finalize_schedule(bot, update):
    global users_to_query, state, scheduling_policies
    global users_dict_id_to_username

    reply_keyboard = [['Yes', 'No', 'You guys go on!']]

    starting_policy_length = len(scheduling_policies)

    if scheduling_policies:
        policy = scheduling_policies[0]
        start = policy.date_from
        end = policy.date_to
        user_ids = policy.users_to_ask

        for user_id in user_ids:

            user = users_dict_id_to_username[user_id]

            if user.id == update.message.from_user.id and bot.id == update.message.reply_to_message.from_user.id:
                if response_text[Responses.AGREE] == update.message.text:
                    text = user.first_name + " can make it"
                    bot.sendMessage(update.message.chat_id, text=text)

                    users_to_query.remove(user.id)
                elif response_text[Responses.DISAGREE] == update.message.text:
                    text = user.first_name + " can't make it. Let's try another option"
                    bot.sendMessage(update.message.chat_id, text=text)
                    scheduling_policies.remove(policy)
                    break
                    # breaking condition
                elif response_text[Responses.FORFEIT] == update.message.text:
                    text = user.first_name + " won't be joining"
                    bot.sendMessage(update.message.chat_id, text=text)

                    users_to_query.remove(user.id)
                else:
                    print "dropped through without processing but captured that the user responded"
                    continue

        # All awkward cases handled we have consensus
        if not users_to_query:
            text = get_text('All participants can make it for the time ', policy.date_from, policy.date_to) + '.'
            bot.sendMessage(update.message.chat_id, text=text)
            scheduling_policies = []
            restart()
            return

        # Ran out of policies and some users still can't make it
        if not scheduling_policies:
            for user_id in users_to_query:
                user = users_dict_id_to_username[user_id]
                text = user.first_name + " can't make the plan"
                bot.sendMessage(update.message.chat_id, text=text)
            bot.sendMessage(update.message.chat_id, text="No plan exists")
            restart()
            return

        # Continue querying other users of the current policy
        elif starting_policy_length == len(scheduling_policies):
            return
        # Announce new policy
        else:
            policy = scheduling_policies[0]

            start = policy.date_from
            end = policy.date_to
            user_ids = policy.users_to_ask

            users_to_query = user_ids[:]

            for user_id in user_ids:

                user = users_dict_id_to_username[user_id]

                if user.username is not "":
                    user_handle = user.username
                else:
                    user_handle = str(user.id) + " (" + user.first_name + ")"

                schedule_text = "@" + user_handle
                schedule_text = schedule_text + get_text(' can you make it ',start,end)+'?'
                #schedule_text = schedule_text + ' can you make it between {} {} and {} {}'.format(
                #    start.strftime(HOUR_FORMAT),
                #    start.strftime(DATA_FORMAT),
                #    end.strftime(HOUR_FORMAT),
                #    end.strftime(DATA_FORMAT))

                bot.sendMessage(update.message.chat_id, text=schedule_text,
                                reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True,
                                                                 one_time_keyboard=True, selective=True))



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

    if state.value < States.FINALIZING.value:
        process_callback[intent](bot,update)
    else:
        finalize_schedule(bot,update)


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
    dp.add_handler(CommandHandler('export', export))


    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


def get_text(string,start,end):
    if start.day == end.day:
        text = string+' between {} and {} on {}'.format(start.strftime(HOUR_FORMAT),
                                               end.strftime(HOUR_FORMAT),
                                              start.strftime(DATA_FORMAT))
    else:
        text = string+' between {} and {}'.format( start.strftime(DATA_FORMAT),
                                                end.strftime(DATA_FORMAT))
    return text

if __name__ == '__main__':
    main()
