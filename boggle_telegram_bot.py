#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
This bot was made by e-caste in 2020
"""

from telegram import ReplyKeyboardMarkup
from telegram.parsemode import ParseMode
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, PicklePersistence)
from telegram.utils.helpers import mention_html
import logging
from secret import token, castes_chat_id, working_directory
from math import ceil
import os
import sys
import traceback
from translations import get_string
from threading import Timer
from dice import get_shuffled_dice
from math import sqrt
from datetime import time
import shutil
from string import whitespace
from contextlib import suppress

HTML = ParseMode.HTML
debug = sys.platform.startswith("darwin")

# Enable logging
level = logging.DEBUG if debug else logging.INFO
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=level)

logger = logging.getLogger(__name__)

newgame_timer_duration = 60  # seconds
timers = {
    'newgame': {},
    'ingame': {}
}

games = {}

# TODO: add logger to each function
def start(update, context):
    reply = get_string(__get_user_lang(context), 'welcome', update.message.from_user.first_name)
    logger.info(f"User {__get_username(update)} started the bot.")
    # if context.user_data:  # TODO: add stats to reply
    #     reply += ""
    context.bot.send_message(chat_id=__get_chat_id(update),
                             text=reply,
                             parse_mode=HTML)


def new(update, context):
    if not __check_chat_is_group(update):
        update.message.reply_text(get_string(__get_user_lang(context), msg='chat_is_not_group'))
    else:
        group_chat_id = __get_chat_id(update)
        if not timers['newgame'].get(group_chat_id):
            t = Timer(interval=newgame_timer_duration, function=__newgame_timer, args=(update, context, group_chat_id))
            t.start()
            timers['newgame'][group_chat_id] = t
            games[group_chat_id] = {
                'creator': {
                    'id': __get_user_id(update),
                    'username': __get_username(update)
                },
                'joined': []
            }
            context.bot.send_message(chat_id=__get_chat_id(update),
                                     text=get_string(__get_user_lang(context), 'game_created', __get_username(update),
                                                     newgame_timer_duration))
        else:
            context.bot.send_message(chat_id=__get_chat_id(update),
                                     text=get_string(__get_user_lang(context), 'game_already_started',
                                                     __get_username(update)))


def join(update, context):
    if not __check_chat_is_group(update):
        update.message.reply_text(get_string(__get_user_lang(context), msg='chat_is_not_group'))
    else:
        group_chat_id = __get_chat_id(update)
        if timers['newgame'].get(group_chat_id):
            if not context.user_data.get(group_chat_id):
                __init_user_stats_for_group(update, context, group_chat_id)
                __join_user_to_game(update, context, group_chat_id)
                context.bot.send_message(chat_id=group_chat_id,
                                         text=get_string(__get_user_lang(context), 'game_joined',
                                                         __get_username(update)))

            elif context.user_data.get(group_chat_id) and context.user_data[group_chat_id]['in_game']:
                context.bot.send_message(chat_id=group_chat_id,
                                         text=get_string(__get_user_lang(context), 'already_in_game',
                                                         __get_username(update),
                                                         games[group_chat_id]['creator']['username']))

            elif context.user_data.get(group_chat_id) and not context.user_data[group_chat_id]['in_game']:
                __join_user_to_game(update, context, group_chat_id)
                context.bot.send_message(chat_id=group_chat_id,
                                         text=get_string(__get_user_lang(context), 'game_joined',
                                                         __get_username(update)))

        else:
            context.bot.send_message(chat_id=__get_chat_id(update),
                                     text=get_string(__get_user_lang(context), msg='no_game_yet'))


def leave(update, context):
    if not __check_chat_is_group(update):
        update.message.reply_text(get_string(__get_user_lang(context), msg='chat_is_not_group'))
    else:
        group_chat_id = __get_chat_id(update)
        if timers['newgame'].get(group_chat_id):
            if not context.user_data.get(group_chat_id):
                __remove_user_from_game(__get_user_id(update), group_chat_id)
                context.bot.send_message(chat_id=group_chat_id,
                                         text=get_string(__get_user_lang(context), 'game_left',
                                                         __get_username(update)))

            elif context.user_data.get(group_chat_id) and context.user_data[group_chat_id]['in_game']:
                __remove_user_from_game(__get_user_id(update), group_chat_id)
                context.bot.send_message(chat_id=group_chat_id,
                                         text=get_string(__get_user_lang(context), 'game_left',
                                                         __get_username(update)))

            elif context.user_data.get(group_chat_id) and not context.user_data[group_chat_id]['in_game']:
                context.bot.send_message(chat_id=group_chat_id,
                                         text=get_string(__get_user_lang(context), 'not_yet_in_game',
                                                         __get_username(update)))

        else:
            context.bot.send_message(chat_id=__get_chat_id(update),
                                     text=get_string(__get_user_lang(context), msg='no_game_yet'))


def start_game(update, context):
    pass



def kick(update, context):
    pass


def kill(update, context):
    pass


def show_statistics(update, context):
    pass


def settings(update, context):
    pass


def show_help(update, context):
    update.message.reply_text(text=get_string(__get_user_lang(context), msg='help'))


def error(update, context):
    """Log Errors caused by Updates."""
    # notify user that experienced the error
    if update.effective_message:
        msg = "Hey. I'm sorry to inform you that an error happened while I tried to handle your update. " \
              "My developer will be notified."
        update.effective_message.reply_text(msg)
    # text the dev
    trace = "".join(traceback.format_tb(sys.exc_info()[2]))
    payload = ""
    # normally, we always have an user. If not, its either a channel or a poll update.
    if update.effective_user:
        payload += " with the user " + str(mention_html(update.effective_user.id, update.effective_user.first_name))
    # there are more situations when you don't get a chat
    if update.effective_chat:
        payload += " within the chat <i>" + str(update.effective_chat.title) + "</i>"
        if update.effective_chat.username:
            payload += " (@" + str(update.effective_chat.username)
    # but only one where you have an empty payload by now: a poll
    if update.poll:
        payload += " with the poll id " + str(update.poll.id)
    # lets put this in a "well" formatted text
    msg = "Hey.\n The error <code>" + str(context.error) + "</code> happened" + str(payload) + \
          ". The full traceback:\n\n<code>" + str(trace) + "</code>"
    context.bot.send_message(chat_id=castes_chat_id,
                             text=msg,
                             parse_mode=HTML)
    raise


def __get_username(update) -> str:
    u = update.message.from_user.username
    u2 = update.message.from_user.first_name
    return "@" + str(u) if u else str(u2)


def __get_user_lang(context) -> str:
    return context.user_data['lang'] if context.user_data.get('lang') else 'eng'


# return True for GROUP or SUPERGROUP, False for PRIVATE (or CHANNEL)
def __check_chat_is_group(update):
    return True if 'group' in update.message.chat.type else False


def __get_chat_id(update) -> int:
    return update.message.chat.id if update.message.chat else update.message.effective_chat.id


def __get_user_id(update) -> int:
    return update.message.from_user.id


def __newgame_timer(update, context, group_chat_id: int):
    if len(games[group_chat_id]['joined']) == 0:
        context.bot.send_message(chat_id=__get_chat_id(update),
                                 text=get_string(__get_user_lang(context), 'newgame_timer_expired'))
        del games[group_chat_id]
    else:
        start_game(update, context)


def __init_user_stats_for_group(update, context, group_chat_id: int):
    d = context.user_data
    d[group_chat_id] = {
        'in_game': True,
        'is_game_creator': True if games[group_chat_id]['creator']['id'] == __get_user_id(update) else False,
        'stats': {
            'matches': {
                'won': {
                    'value': 0,
                    'percentage': 0
                },
                'even': {
                    'value': 0,
                    'percentage': 0
                },
                'lost': {
                    'value': 0,
                    'percentage': 0
                },
                'last': {
                    'value': 0,
                    'percentage': 0
                },
                'played': 0
            },
            'points': {
                'last_match': 0,
                'average': 0,
                'total': 0
            }
        }
    }


def __join_user_to_game(update, context, group_chat_id: int):
    games[group_chat_id]['joined'].append({
        'id': __get_user_id(update),
        'username': __get_username(update),
        'user_data': context.user_data
    })


def __remove_user_from_game(user_chat_id: int, group_chat_id: int):
    joined = games[group_chat_id]['joined']
    for user in joined:
        if user_chat_id == user['id']:
            joined.remove(user)
            break


def __get_formatted_table(shuffled_dice: list) -> str:
    # assuming the table is always an NxN square
    total_num = len(shuffled_dice)
    row_col_num = int(sqrt(total_num))
    formatted_table = "<b>"
    for i in range(0, total_num, row_col_num):
        formatted_table += "  ".join(shuffled_dice[i:i + row_col_num]) + "\n"
    formatted_table += "</b>"
    return formatted_table


def main():
    pp = PicklePersistence(filename='_boggle_paroliere_bot_db')
    updater = Updater(token, persistence=pp, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start, pass_user_data=True))
    dp.add_handler(CommandHandler('new', new, pass_user_data=True))
    dp.add_handler(CommandHandler('join', join, pass_user_data=True))
    dp.add_handler(CommandHandler('startgame', start_game, pass_user_data=True))
    dp.add_handler(CommandHandler('leave', leave, pass_user_data=True))
    dp.add_handler(CommandHandler('kick', kick, pass_user_data=True))
    dp.add_handler(CommandHandler('kill', kill, pass_user_data=True))
    dp.add_handler(CommandHandler('stats', show_statistics, pass_user_data=True))
    dp.add_handler(CommandHandler('settings', settings, pass_user_data=True))
    dp.add_handler(CommandHandler('help', show_help, pass_user_data=True))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    if not debug:
        os.chdir(working_directory)
    main()
