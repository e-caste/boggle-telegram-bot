#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
This bot was made by e-caste in 2020
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.parsemode import ParseMode
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackQueryHandler, PicklePersistence)
from telegram.utils.helpers import mention_html
from telegram.error import Unauthorized
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


def bot_added_to_group(update, context):
    if update.message.new_chat_members[0].username == context.bot.username:
        context.bot.send_message(chat_id=__get_chat_id(update),
                                 text=get_string(__get_chat_lang(context), 'bot_added_to_group'),
                                 parse_mode=HTML)


def new(update, context):
    __check_bot_data_is_initialized(context)

    if not __check_chat_is_group(update):
        update.message.reply_text(get_string(__get_chat_lang(context), msg='chat_is_not_group'))
        return

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
            'participants': {},
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
        return

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

        if current_game['participants'].get(user_id):
            context.bot.send_message(chat_id=group_chat_id,
                                     text=get_string(__get_chat_lang(context), 'already_in_game',
                                                     __get_username(update),
                                                     current_game['creator']['username']))
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
        return

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

        if current_game['participants'].get(user_id):
            __remove_user_from_game(update, context)
            context.bot.send_message(chat_id=group_chat_id,
                                     text=get_string(__get_chat_lang(context), 'game_left',
                                                     __get_username(update)))
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

    if not __check_chat_is_group(update):
        context.bot.send_message(chat_id=group_chat_id,
                                 text=get_string(__get_chat_lang(context), 'chat_is_not_group'))
        return

    if current_game is None:
        context.bot.send_message(chat_id=group_chat_id,
                                 text=get_string(__get_chat_lang(context), 'no_game_yet'))
        return

    if not timer:
        if __forbid_not_game_creator(update, context, command="/startgame"):
            return
        else:
            cd['timers']['newgame'] = None
            timers['newgame'][group_chat_id]()  # cancel timer if started by game creator

    table_list = get_shuffled_dice(cd['settings']['lang'], cd['settings']['table_dimensions'])
    table_str = __get_formatted_table(table_list)

    row_col_num = int(sqrt(len(table_list)))
    table_list = [letter if letter != "Qu" else "Q" for letter in table_list]
    table_grid = {(row, col): table_list[row * row_col_num + col].lower()
                  for row in range(row_col_num) for col in range(row_col_num)}

    bd['games'][group_chat_id] = current_game
    bd['games'][group_chat_id]['table_grid'] = table_grid

    context.bot.send_message(chat_id=group_chat_id,
                             text=get_string(__get_chat_lang(context), 'game_started_group'))

    text = get_string(__get_chat_lang(context), 'game_started_private',
                      cd['timers']['durations']['ingame']) + "\n\n\n" + table_str
    for player in current_game['participants']:
        try:
            context.bot.send_message(chat_id=player,
                                     text=text,
                                     parse_mode=HTML)
        except Unauthorized:
            context.bot.send_message(chat_id=group_chat_id,
                                     text=get_string(__get_chat_lang(context), 'bot_not_started_by_user',
                                                     current_game['participants'][player]['username']))
            kill(update, context)  # TODO: implement

    t = Timer(interval=cd['timers']['durations']['ingame'],
              function=__ingame_timer, args=(update, context, group_chat_id))
    t.start()
    bd['games'][group_chat_id]['ingame_timer'] = t.name
    timers['ingame'][group_chat_id] = t.cancel


def points_handler(update, context):
    __check_bot_data_is_initialized(context)

    chat_id = __get_chat_id(update)
    user_id = __get_user_id(update)
    bd = context.bot_data

    not_finished = {}
    for game in bd['games']:
        if not bd['games'][game]['is_finished']:
            not_finished[game] = bd['games'][game]

    for group in not_finished:
        participants = bd['games'][group]['participants']
        for participant in participants:
            if user_id == participant:
                group_id = group
                break
        else:
            continue
        break
    else:
        context.bot.send_message(chat_id=chat_id,
                                 text=get_string(__get_chat_lang(context), 'received_dm_but_user_not_in_game'))
        return

    word = update.message.text.lower()

    for char in word:
        if char not in letters_sets[bd['games'][group_id]['lang']]:
            update.message.reply_text(get_string(__get_game_lang(context, group_id), 'received_dm_but_char_not_alpha'))
            return

    if len(word) < 3:
        update.message.reply_text(get_string(__get_game_lang(context, group_id), 'received_dm_but_word_too_short'))
        return

    if "q" in word and "qu" not in word:
        update.message.reply_text(get_string(__get_game_lang(context, group_id), 'received_dm_but_q_without_u'))
        return

    word = word.replace("qu", "q")

    if not __validate_word_by_boggle_rules(word, bd['games'][group_id]['table_grid']):
        update.message.reply_text(get_string(__get_game_lang(context, group_id), 'received_dm_but_word_not_validated'))
        return

    word = word.replace("q", "qu")
    words = bd['games'][group_id]['participants'][user_id]['words']

    if not words.get(word):
        words[word] = {
            'points': __get_points_for_word(word),
            'sent_by_other_players': False,
            'deleted': False
        }
    else:
        update.message.reply_text(get_string(__get_game_lang(context, group_id), 'received_dm_but_word_already_sent',
                                             word))


def delete(update, context):
    __check_bot_data_is_initialized(context)

    if not __check_chat_is_group(update):
        update.message.reply_text(get_string(__get_chat_lang(context), msg='chat_is_not_group'))
        return

    user_id = __get_user_id(update)
    group_id = __get_chat_id(update)
    bd = context.bot_data

    if not bd['games'].get(group_id):
        update.message.reply_text(get_string(__get_chat_lang(context), msg='no_game_yet'))
        return

    game = bd['games'][group_id]
    lang = game['lang']

    if user_id != game['creator']['id']:
        update.message.reply_text(get_string(lang, 'forbid_not_game_creator',
                                             __get_username(update), game['creator']['username'], "/delete"))
        return

    if not game['is_finished']:
        update.message.reply_text(get_string(lang, msg='game_not_yet_finished'))
        return

    words = update.message.text.lower().split()[1:]  # skip /delete

    for word in words:
        for char in word:
            if char not in letters_sets[lang]:
                update.message.reply_text(get_string(lang, 'char_not_alpha', word))
                return

    not_found = words
    players = game['participants']
    for user_id in players:
        player_words = [w for w in players[user_id]['words']]
        for player_word in player_words:
            for word in words:
                if player_word == word:
                    players[user_id]['words'][player_word]['deleted'] = True
                    not_found.remove(word)

    if len(not_found) > 0:
        update.message.reply_text(get_string(lang, 'words_not_found_in_players_words', not_found))
    else:
        update.message.reply_text(get_string(lang, 'all_words_deleted'))


def end_game(update, context):
    __check_bot_data_is_initialized(context)

    if not __check_chat_is_group(update):
        update.message.reply_text(get_string(__get_chat_lang(context), msg='chat_is_not_group'))
        return

    user_id = __get_user_id(update)
    group_id = __get_chat_id(update)
    cd = context.chat_data
    bd = context.bot_data

    if not bd['games'].get(group_id):
        update.message.reply_text(get_string(__get_chat_lang(context), msg='no_game_yet'))
        return

    game = bd['games'][group_id]
    lang = game['lang']

    if user_id != game['creator']['id']:
        update.message.reply_text(get_string(lang, 'forbid_not_game_creator',
                                             __get_username(update), game['creator']['username'], "/endgame"))
        return

    if not game['is_finished']:
        update.message.reply_text(get_string(lang, msg='game_not_yet_finished'))
        return

    us = bd['stats']['users']
    gs = bd['stats']['groups']

    total_points = 0
    players_points = {}
    players = game['participants']
    for user_id in players:  # stats already initialized in join()
        words = players[user_id]['words']
        for word in words:
            if not words[word]['sent_by_other_players'] and not words[word]['deleted']:
                if not players_points.get(user_id):
                    players_points[user_id] = words[word]['points']
                else:
                    players_points[user_id] += words[word]['points']
                total_points += words[word]['points']
        if not players_points.get(user_id):  # hasn't made any points
            players_points[user_id] = 0

    max_points = -1
    for user_id in players_points:
        points = players_points[user_id]
        max_points = points if points > max_points else max_points

    winners = {}
    for user_id in players_points:
        if players_points[user_id] == max_points:
            winners[user_id] = game['participants'][user_id]['username']
    game['winners'] = winners

    # update group stats
    if not gs.get(group_id):
        gs[group_id] = {
            'matches': 0,
            'points': 0,
            'average': 0
        }
    gs[group_id]['points'] += total_points
    gs[group_id]['matches'] += 1
    gs[group_id]['average'] = int(gs[group_id]['points'] / gs[group_id]['matches'])

    # update users stats
    for user_id in players:
        us[user_id]['matches']['played'] += 1
        if winners.get(user_id) and len(winners) == 1:  # won
            us[user_id]['matches']['won']['value'] += 1
        elif winners.get(user_id) and len(winners) > 1:  # even
            us[user_id]['matches']['even']['value'] += 1
        elif not winners.get(user_id):  # lost
            us[user_id]['matches']['lost']['value'] += 1
        for ending in ['won', 'even', 'lost']:
            us[user_id]['matches'][ending]['percentage'] = round(us[user_id]['matches'][ending]['value']
                                                                 / us[user_id]['matches']['played'] * 100, 2)
        us[user_id]['points']['max'] = players_points[user_id] if players_points[user_id] > us[user_id]['points']['max'] \
            else us[user_id]['points']['max']
        us[user_id]['points']['min'] = players_points[user_id] if players_points[user_id] < us[user_id]['points']['max'] \
            else us[user_id]['points']['min']
        us[user_id]['points']['last_match'] = players_points[user_id]
        us[user_id]['points']['total'] += players_points[user_id]
        us[user_id]['points']['average'] = round(us[user_id]['points']['total'] / us[user_id]['matches']['played'], 2)

    chat_game = __get_latest_game(context)
    cd['games'].remove(chat_game)
    cd['games'].append(game)
    del bd['games'][group_id]

    lang = __get_chat_lang(context)
    winner_str = ""
    if len(winners) == 1:
        winner_str = get_string(lang, 'game_winner_singular')
    elif len(winners) > 1:
        winner_str = get_string(lang, 'game_winners_plural')

    winners_usernames = ""
    for user_id in winners:
        winners_usernames += winners[user_id] + ", "
    winners_usernames = winners_usernames[:-2]

    context.bot.send_message(chat_id=group_id,
                             text=get_string(lang, 'game_finished',
                                             winner_str, winners_usernames, max_points),
                             parse_mode=HTML)


def kick(update, context):
    __check_bot_data_is_initialized(context)

    if __check_chat_is_group(update):
        update.message.reply_text(get_string(__get_chat_lang(context), msg='chat_is_not_group'))
        return

    bd = context.bot_data
    user_id = __get_user_id(update)
    group_id = __get_chat_id(update)

    if not bd['games'].get(group_id):
        update.message.reply_text(get_string(__get_chat_lang(context), msg='no_game_yet'))
        return

    game = bd['games'][group_id]
    lang = game['lang']

    if user_id != game['creator']['id']:
        update.message.reply_text(get_string(lang, 'forbid_not_game_creator',
                                             __get_username(update), game['creator']['username'], "/kick"))
        return

    if game['is_finished']:
        update.message.reply_text(get_string(lang, 'game_already_finished_kick', game['creator']['username']))
        return

    reply_keyboard = [[]]
    for user_id in game['participants']:
        button = InlineKeyboardButton(game['participants'][user_id]['username'],
                                      callback_data=f"kick_{user_id}_from_{group_id}")
        if len(reply_keyboard[-1]) == 2:
            reply_keyboard.append([button])
        else:
            reply_keyboard[-1].append(button)
    reply_markup = InlineKeyboardMarkup(reply_keyboard)

    context.bot.send_message(chat_id=group_id,
                             text=get_string(lang, 'kick_user_choice_group', game['creator']['username']),
                             reply_markup=reply_markup)


def kill(update, context):
    __check_bot_data_is_initialized(context)

    if not __check_chat_is_group(update):
        update.message.reply_text(get_string(__get_chat_lang(context), msg='chat_is_not_group'))
        return

    bd = context.bot_data
    cd = context.chat_data
    user_id = __get_user_id(update)
    group_id = __get_chat_id(update)

    if not bd['games'].get(group_id):
        update.message.reply_text(get_string(__get_chat_lang(context), msg='no_game_yet'))
        return

    game = bd['games'][group_id]
    lang = game['lang']

    if user_id != game['creator']['id']:
        update.message.reply_text(get_string(lang, 'forbid_not_game_creator',
                                             __get_username(update), game['creator']['username'], "/kill"))
        return

    if game['is_finished']:
        update.message.reply_text(get_string(lang, 'game_already_finished_kill', game['creator']['username']))
        return

    context.bot.send_message(chat_id=group_id,
                             text=get_string(lang, 'game_killed_group'))

    for user_id in game['participants']:
        context.bot.send_message(chat_id=user_id,
                                 text=get_string(lang, 'game_killed_private', game['creator']['username']))

    del bd['games'][group_id]
    latest_game = __get_latest_game(context)
    cd['games'].remove(latest_game)



def show_statistics(update, context):
    __check_bot_data_is_initialized(context)
    # TODO: if in group chat, ask the user if he wants group or their stats
    # TODO: if in private chat, show the user's stats
    pass


def settings(update, context):
    __check_bot_data_is_initialized(context)
    pass


def show_rules(update, context):
    __check_bot_data_is_initialized(context)
    context.bot.send_message(chat_id=__get_chat_id(update),
                             text=get_string(__get_chat_lang(context), 'rules'),
                             parse_mode=HTML)


def show_usage(update, context):
    __check_bot_data_is_initialized(context)
    context.bot.send_message(chat_id=__get_chat_id(update),
                             text=get_string(__get_chat_lang(context), 'usage'),
                             parse_mode=HTML)


def show_help(update, context):
    __check_bot_data_is_initialized(context)
    update.message.reply_text(text=get_string(__get_chat_lang(context), msg='help'))


def query_handler(update, context):
    query = update.callback_query
    user_id = query.message.from_user.id
    bd = context.bot_data

    if query.data.startswith("kick"):
        user_id_to_kick = int(query.data.split("kick_")[1].split("_from_")[0])
        group_id_to_kick_from = int(query.data.split("_from_")[1])
        game = bd['games'][group_id_to_kick_from]

        if user_id != game['creator']['id']:
            context.bot.send_message(chat_id=group_id_to_kick_from,
                                     text="Only the game creator can choose who to kick!")
            return

        lang = __get_game_lang(context, group_id_to_kick_from)

        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text=get_string(lang,
                                                      'kick_user_successful',
                                                      game['participants'][user_id_to_kick]['username']))

        try:
            context.bot.send_message(chat_id=user_id_to_kick,
                                     text=get_string(lang, 'you_have_been_kicked', game['creator']['username']))
        except Unauthorized:
            pass

        del game['participants'][user_id_to_kick]


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


def __get_game_lang(context, group_id: int) -> str:
    bd = context.bot_data
    return bd['games'][group_id]['lang']


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


def __ingame_timer(update, context, group_id: int):
    game = context.bot_data['games'][group_id]
    game['ingame_timer'] = None
    game['is_finished'] = True
    __check_words_in_common(context, group_id)
    player_words_with_points = {}
    for user_id in game['participants']:  # TODO: check why this function does not return the correct string
        player_words_with_points[user_id] = __get_formatted_words(context, group_id, with_points=True, user_id=user_id)
    player_words_without_points = __get_formatted_words(context, group_id, with_points=False)

    for user_id in player_words_with_points:
        context.bot.send_message(chat_id=user_id,
                                 text=get_string(__get_game_lang(context, group_id), 'ingame_timer_expired_private',
                                                 player_words_with_points[user_id]),
                                 parse_mode=HTML)

    context.bot.send_message(chat_id=group_id,
                             text=get_string(__get_chat_lang(context), 'ingame_timer_expired_group',
                                             game['creator']['username'], game['creator']['username'],
                                             player_words_without_points),
                             # .replace("<", "&lt;").replace(">", "&gt;").replace("'", "&#39;"),
                             parse_mode=HTML)
    # TODO: fix telegram.error.BadRequest: Can't parse entities: unsupported start tag "list" at byte offset 212


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
            'ingame': 30  # seconds  # TODO: change to 180
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
            # 'last': {
            #     'value': 0,
            #     'percentage': 0
            # },
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
    user_id = __get_user_id(update)
    cd['ingame_user_ids'].append(user_id)
    current_game = __get_current_game(context)
    current_game['participants'][user_id] = {
        'username': __get_username(update),
        'words': {}
    }


def __remove_user_from_game(update, context):
    cd = context.chat_data
    current_game = __get_current_game(context)
    participants = current_game['participants']
    user_id = __get_user_id(update)
    cd['ingame_user_ids'].remove(user_id)
    del participants[user_id]


def __get_latest_game(context) -> dict:
    cd = context.chat_data
    res = {'unix_epoch': 0}
    if cd.get('games'):
        for game in cd['games']:
            res = game if game['unix_epoch'] > res['unix_epoch'] else res
        return res
    res['is_finished'] = True
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
                break

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
    for i, letter in enumerate(table):
        table[i] = letter.lower()
    res = []
    total_num = len(table)
    row_col_num = int(sqrt(total_num))
    for i in range(0, total_num, row_col_num):
        res.append(table[i:i + row_col_num])
    return res


def __validate_word_by_boggle_rules(word: str, grid: dict) -> bool:
    neighbours = __get_all_grid_neighbours(grid)
    paths = []
    full_words = set()
    full_words.add(word)
    stems = set(word[:i] for i in range(1, len(word)))

    def __do_search(path):
        word = __get_path_to_word(grid, path)
        if word in full_words:
            paths.append(path)
        if word not in stems:
            return
        for next_pos in neighbours[path[-1]]:
            if next_pos not in path:
                __do_search(path + [next_pos])

    for position in grid:
        __do_search([position])

    words = set()
    for path in paths:
        words.add(__get_path_to_word(grid, path))

    return word in words


def __get_all_grid_neighbours(grid: dict) -> dict:
    neighbours = {}
    for position in grid:
        position_neighbours = __get_neighbours_of_position(position)
        neighbours[position] = [p for p in position_neighbours if p in grid]
    return neighbours


def __get_neighbours_of_position(coords: tuple) -> list:
    row, col = coords

    top_left = (row - 1, col - 1)
    top_center = (row - 1, col)
    top_right = (row - 1, col + 1)

    left = (row, col - 1)
    right = (row, col + 1)

    bottom_left = (row + 1, col - 1)
    bottom_center = (row + 1, col)
    bottom_right = (row + 1, col + 1)

    return [top_left, top_center, top_right,
            left, right,
            bottom_left, bottom_center, bottom_right]


def __get_path_to_word(grid: dict, path: list) -> str:
    return ''.join([grid[p] for p in path])


def __get_points_for_word(word: str) -> int:
    length = len(word)
    if length < 3:
        return 0
    elif length == 3 or length == 4:
        return 1
    elif length == 5:
        return 2
    elif length == 6:
        return 3
    elif length == 7:
        return 5
    else:
        return 11


def __check_words_in_common(context, group_id: int):
    players = context.bot_data['games'][group_id]['participants']
    players_2 = players.copy()
    for player in players:
        del players_2[player]
        words = players[player]['words']
        for word in words:
            if not words[word]['sent_by_other_players']:
                for player_2 in players_2:
                    words_2 = players_2[player_2]['words']
                    for word_2 in words_2:
                        if not words[word]['sent_by_other_players']:
                            if word == word_2:
                                words[word]['sent_by_other_players'] = True
                                words_2[word_2]['sent_by_other_players'] = True


def __get_formatted_words(context, group_id: int, with_points: bool, user_id: int = None) -> str:
    players = context.bot_data['games'][group_id]['participants']
    res = ""

    def __get_formatted_words_internal(res) -> str:
        res += f"<b>{players[player]['username']}</b>\n"
        words = players[player]['words']
        for word in words:
            if words[word]['sent_by_other_players']:
                res += "<strike>"
            else:
                res += "<i>"
            res += f"{word}"
            if with_points:
                res += f": {words[word]['points']}"
            if words[word]['sent_by_other_players']:
                res += "</strike>"
            else:
                res += "</i>"
            res += "\n"
        return res

    for player in players:
        if user_id:
            if player == user_id:
                res = __get_formatted_words_internal(res)
                return res
        else:
            res = __get_formatted_words_internal(res)
            res += "\n\n"
    return res


def main():
    pp = PicklePersistence(filename='_boggle_paroliere_bot_db')
    updater = Updater(token, persistence=pp, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # TODO: add greetings message when the bot gets added to a group
    # TODO: add init function that tells all players in games during bot's restart they have to begin the game again,
    #  and deletes all context.bot_data['games'] and context.chat_data current_game
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('new', new))
    dp.add_handler(CommandHandler('join', join))
    dp.add_handler(CommandHandler('startgame', start_game))
    dp.add_handler(CommandHandler('delete', delete))
    dp.add_handler(CommandHandler('endgame', end_game))
    dp.add_handler(CommandHandler('leave', leave))
    dp.add_handler(CommandHandler('kick', kick))
    dp.add_handler(CommandHandler('kill', kill))
    dp.add_handler(CommandHandler('stats', show_statistics))
    dp.add_handler(CommandHandler('settings', settings))
    dp.add_handler(CommandHandler('rules', show_rules))
    dp.add_handler(CommandHandler('usage', show_usage))
    dp.add_handler(CommandHandler('help', show_help))

    # handles all text messages in a private chat
    dp.add_handler(MessageHandler(Filters.text & ~ Filters.group, points_handler))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, bot_added_to_group))

    # handles callback queries from InlineKeyboardButtons
    dp.add_handler(CallbackQueryHandler(query_handler))

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
