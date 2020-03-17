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
from dice import get_shuffled_dice, letters_sets
from math import sqrt
from time import time
# from datetime import time
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

timers = {
    'newgame': {},
    'ingame': {}
}

# TODO: add logger to each function
def start(update, context):
    __check_bot_data_is_initialized(context)

    reply = get_string(__get_chat_lang(context), 'welcome', update.message.from_user.first_name)
    logger.info(f"User {__get_username(update)} started the bot.")
    # if context.user_data:  # TODO: add stats to reply
    #     reply += ""
    context.bot.send_message(chat_id=__get_chat_id(update),
                             text=reply,
                             parse_mode=HTML)


def new(update, context):
    __check_bot_data_is_initialized(context)

    if not __check_chat_is_group(update):
        update.message.reply_text(get_string(__get_chat_lang(context), msg='chat_is_not_group'))
    else:
        group_chat_id = __get_chat_id(update)
        cd = context.chat_data
        if not cd.get('timers'):
            __init_chat_data(context)

        if not cd['timers']['newgame']:
            t = Timer(interval=cd['timers']['durations']['newgame'],
                      function=__newgame_timer, args=(update, context))
            t.start()
            cd['timers']['newgame'] = t.name
            timers['newgame'][group_chat_id] = t.cancel  # pass callable
            cd['games'].append({
                'unix_epoch': int(time()),
                'creator': {
                    'id': __get_user_id(update),
                    'username': __get_username(update)
                },
                'participants': [],
                'is_finished': False,
                'ingame_timer': None,
                'lang': __get_chat_lang(context)
            })
            context.bot.send_message(chat_id=__get_chat_id(update),
                                     text=get_string(__get_chat_lang(context), 'game_created', __get_username(update),
                                                     cd['timers']['durations']['newgame']))
        else:
            context.bot.send_message(chat_id=__get_chat_id(update),
                                     text=get_string(__get_chat_lang(context), 'game_already_created',
                                                     __get_username(update)))


def join(update, context):
    __check_bot_data_is_initialized(context)

    if not __check_chat_is_group(update):
        update.message.reply_text(get_string(__get_chat_lang(context), msg='chat_is_not_group'))
    else:
        group_chat_id = __get_chat_id(update)
        cd = context.chat_data
        if not cd.get('timers'):
            __init_chat_data(context)
            context.bot.send_message(chat_id=__get_chat_id(update),
                                     text=get_string(__get_chat_lang(context), msg='no_game_yet'))
            return

        bd = context.bot_data
        # TODO: add check that the user joining has started the bot in a private chat

        if cd['timers']['newgame']:
            current_game = __get_current_game(context)
            user_id = __get_user_id(update)

            for participant in current_game['participants']:
                if user_id == participant['id']:
                    context.bot.send_message(chat_id=group_chat_id,
                                             text=get_string(__get_chat_lang(context), 'already_in_game',
                                                             __get_username(update),
                                                             current_game['creator']['username']))
                    break
            else:
                if group_chat_id not in bd['stats']['groups']:
                    __init_group_stats(context, group_chat_id)

                if not bd['stats']['users'].get(user_id):  # user has never played
                    __init_user_stats(context, user_id, __get_username(update), group_chat_id, new_player=True)
                elif not bd['stats']['groups'][group_chat_id].get(user_id):  # user has already played in other groups
                    __init_user_stats(context, user_id, __get_username(update), group_chat_id, new_player=False)

                __join_user_to_game(update, context)
                context.bot.send_message(chat_id=group_chat_id,
                                         text=get_string(__get_chat_lang(context), 'game_joined',
                                                         __get_username(update), current_game['creator']['username']))

        else:
            context.bot.send_message(chat_id=__get_chat_id(update),
                                     text=get_string(__get_chat_lang(context), msg='no_game_yet'))


def leave(update, context):
    __check_bot_data_is_initialized(context)

    if not __check_chat_is_group(update):
        update.message.reply_text(get_string(__get_chat_lang(context), msg='chat_is_not_group'))
    else:
        group_chat_id = __get_chat_id(update)
        cd = context.chat_data
        if not cd.get('timers'):
            __init_chat_data(context)
            context.bot.send_message(chat_id=__get_chat_id(update),
                                     text=get_string(__get_chat_lang(context), msg='no_game_yet'))
            return

        if cd['timers']['newgame']:
            current_game = __get_current_game(context)
            user_id = __get_user_id(update)

            for participant in current_game['participants']:
                if user_id == participant['id']:
                    __remove_user_from_game(update, context)
                    context.bot.send_message(chat_id=group_chat_id,
                                             text=get_string(__get_chat_lang(context), 'game_left',
                                                             __get_username(update)))
                    break
            else:
                context.bot.send_message(chat_id=group_chat_id,
                                         text=get_string(__get_chat_lang(context), 'not_yet_in_game',
                                                         __get_username(update)))

        else:
            context.bot.send_message(chat_id=__get_chat_id(update),
                                     text=get_string(__get_chat_lang(context), msg='no_game_yet'))


def start_game(update, context, timer: bool = False):
    __check_bot_data_is_initialized(context)

    cd = context.chat_data
    bd = context.bot_data
    current_game = __get_current_game(context)
    group_chat_id = __get_chat_id(update)
    if not timer:
        if __forbid_not_game_creator(update, context, command="/startgame"):
            return
        else:
            cd['timers']['newgame'] = None
            timers['newgame'][group_chat_id]()  # cancel timer if started by game creator

    table_list = get_shuffled_dice(cd['settings']['lang'], cd['settings']['table_dimensions'])
    table_str = __get_formatted_table(table_list)

    bd['games'][group_chat_id] = current_game
    bd['games'][group_chat_id]['table'] = __convert_table_list_to_matrix(table_list)

    context.bot.send_message(chat_id=group_chat_id,
                             text=get_string(__get_chat_lang(context), 'game_started_group'))
    for player in current_game['participants']:
        context.bot.send_message(chat_id=player['id'],
                                 text=get_string(__get_chat_lang(context), 'game_started_private',
                                                 cd['timers']['durations']['ingame']) + "\n\n\n" + table_str,
                                 parse_mode=HTML)

    t = Timer(interval=cd['timers']['durations']['newgame'],
              function=__ingame_timer, args=(update, context))
    t.start()
    bd['games'][group_chat_id]['ingame_timer'] = t.name
    timers['ingame'][group_chat_id] = t.cancel


def points_handler(update, context):
    chat_id = __get_chat_id(update)
    user_id = __get_user_id(update)
    bd = context.bot_data

    for group in bd['games']:
        for participant in group['participants']:
            if user_id == participant['id']:
                group_dict = group
                break
        else:
            continue
        break
    else:
        context.bot.send_message(chat_id=chat_id,
                                 text=get_string(__get_chat_lang(context), 'received_dm_but_user_not_in_game'))
        return

    word = update.message.text
    if set(word) > letters_sets[group_dict['lang']]:
        update.message.reply_text(get_string(__get_chat_lang(context), 'received_dm_but_char_not_alpha'))
        return






def kick(update, context):
    __check_bot_data_is_initialized(context)
    pass


def kill(update, context):
    __check_bot_data_is_initialized(context)
    pass


def show_statistics(update, context):
    __check_bot_data_is_initialized(context)
    # TODO: if in group chat, ask the user if he wants group or their stats
    # TODO: if in private chat, show the user's stats
    pass


def settings(update, context):
    __check_bot_data_is_initialized(context)
    pass


def show_help(update, context):
    __check_bot_data_is_initialized(context)
    update.message.reply_text(text=get_string(__get_chat_lang(context), msg='help'))


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
    return "@" + str(u) if u else str(u2)  # TODO: check if @ can be used with the first_name


def __get_chat_lang(context) -> str:
    cd = context.chat_data
    return cd['settings']['lang'] if cd.get('settings') else 'eng'


# return True for GROUP or SUPERGROUP, False for PRIVATE (or CHANNEL)
def __check_chat_is_group(update):
    return 'group' in update.message.chat.type


def __get_chat_id(update) -> int:
    return update.message.chat.id if update.message.chat else update.message.effective_chat.id


def __get_user_id(update) -> int:
    return update.message.from_user.id


def __newgame_timer(update, context):
    cd = context.chat_data
    current_game = __get_current_game(context)
    cd['timers']['newgame'] = None
    if len(current_game['participants']) == 0:
        context.bot.send_message(chat_id=__get_chat_id(update),
                                 text=get_string(__get_chat_lang(context), 'newgame_timer_expired'))
        cd['games'].remove(current_game)
    else:
        start_game(update, context, timer=True)


def __ingame_timer(update, context):
    pass


def __check_bot_data_is_initialized(context):
    if not context.bot_data.get('stats'):
        __init_bot_data(context)


def __init_bot_data(context):
    bd = context.bot_data
    bd['games'] = {}
    bd['stats'] = {
        'users': {},
        'groups': {}
    }


def __init_chat_data(context):
    cd = context.chat_data
    cd['timers'] = {
        'newgame': None,
        'ingame': None,
        'durations': {
            'newgame': 90,  # seconds
            'ingame': 180  # seconds
        }
    }
    cd['games'] = []
    cd['ingame_user_ids'] = []
    cd['settings'] = {
        'lang': 'eng',
        'table_dimensions': '4x4'
    }


def __init_group_stats(context, group_id: int):
    bd = context.bot_data
    bd['stats']['groups'][group_id] = {
        'matches': 0,
        'points': 0,
        'average': 0
    }


def __init_user_stats(context, user_id: int, username: str, group_id: int, new_player: bool):
    bd = context.bot_data
    initial_stats = {
        'username': username,
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
            'max': 0,
            'min': 0,
            'last_match': 0,
            'average': 0,
            'total': 0
        }
    }
    if new_player:
        bd['stats']['users'][user_id] = initial_stats
    bd['stats']['groups'][group_id][user_id] = initial_stats


def __join_user_to_game(update, context):
    cd = context.chat_data
    cd['ingame_user_ids'].append(__get_user_id(update))
    current_game = __get_current_game(context)
    current_game['participants'].append({
        'id': __get_user_id(update),
        'username': __get_username(update)
    })


def __remove_user_from_game(update, context):
    cd = context.chat_data
    current_game = __get_current_game(context)
    participants = current_game['participants']
    user_id = __get_user_id(update)
    cd['ingame_user_ids'].remove(user_id)
    for user in participants:
        if user_id == user['id']:
            participants.remove(user)
            break


def __get_latest_game(context) -> dict:
    cd = context.chat_data
    res = {'unix_epoch': 0}
    for game in cd['games']:
        res = game if game['unix_epoch'] > res['unix_epoch'] else res
    return res


def __get_current_game(context) -> dict:
    res = __get_latest_game(context)
    return res if not res['is_finished'] else None


def __forbid_not_game_creator(update, context, command: str) -> bool:
    current_game = __get_current_game(context)
    user_id = __get_user_id(update)
    if user_id != current_game['creator']['id']:
        context.bot.send_message(chat_id=__get_chat_id(update),
                                 text=get_string(__get_chat_lang(context), 'forbid_not_game_creator',
                                                 __get_username(update), current_game['creator']['username'], command))
        return True
    return False


def __get_formatted_table(shuffled_dice: list) -> str:
    # assuming the table is always an NxN square
    total_num = len(shuffled_dice)
    row_col_num = int(sqrt(total_num))

    Qu_is_in_table = "Qu" in shuffled_dice

    formatted_table = ""
    for i in range(0, total_num, row_col_num):
        formatted_table += "  |  ".join(shuffled_dice[i:i + row_col_num]) + "\n"
        if i != total_num - row_col_num:
            formatted_table += "---|--" * (row_col_num - 1) + "-\n"

    if Qu_is_in_table:
        lines = formatted_table.splitlines()
        formatted_table = ""
        index_u = -1
        for line in lines:
            if "Qu" in line:
                index_u = line.index("u")

        for line in lines:
            if "Qu" not in line:
                formatted_table += line[:index_u]
                if "-" not in line:
                    formatted_table += " "
                else:
                    formatted_table += "-"
                formatted_table += line[index_u:]
            else:
                formatted_table += line
            formatted_table += "\n"

    return "<code>" + formatted_table + "</code>"


def __convert_table_list_to_matrix(table: list) -> list:
    res = []
    total_num = len(table)
    row_col_num = int(sqrt(total_num))
    for i in range(0, total_num, row_col_num):
        res.append(table[i:i + row_col_num])
    return res


def main():
    pp = PicklePersistence(filename='_boggle_paroliere_bot_db')
    updater = Updater(token, persistence=pp, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # TODO: add greetings message when the bot gets added to a group
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('new', new))
    dp.add_handler(CommandHandler('join', join))
    dp.add_handler(CommandHandler('startgame', start_game))
    dp.add_handler(CommandHandler('leave', leave))
    dp.add_handler(CommandHandler('kick', kick))
    dp.add_handler(CommandHandler('kill', kill))
    dp.add_handler(CommandHandler('stats', show_statistics))
    dp.add_handler(CommandHandler('settings', settings))
    dp.add_handler(CommandHandler('help', show_help))

    # handles all text messages in a private chat
    dp.add_handler(MessageHandler(Filters.text & ~ Filters.group, points_handler))

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
    else:
        os.remove('_boggle_paroliere_bot_db')
    main()
