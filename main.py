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
import logging

from settigns import TOKEN
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start_consensus(bot, update):
    """Cleans/initializes data structures (runs new reasoning)

    :param bot:
    :param update:
    :return:
    """
    raise NotImplemented
    #bot.sendMessage(update.message.chat_id, text='Hi!')


def end_consensus(bot, update):
    """Returns reasoning result (in future it will be running bot queries)

    :param bot:
    :param update:
    :return:
    """
    raise NotImplemented
    #bot.sendMessage(update.message.chat_id, text='Help!')


def times(bot, update):
    """Adds data entities proposed by user

    :param bot:
    :param update:
    :return:
    """
    raise NotImplemented
    #bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.warn('Update {} caused error {}'.format(update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

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
