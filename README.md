# boggle-telegram-bot
[![Supported Python versions](https://img.shields.io/badge/python-3.6-brightgreen)]() [![GitHub license](https://img.shields.io/github/license/e-caste/boggle-telegram-bot)](https://github.com/e-caste/boggle-telegram-bot/blob/master/LICENSE)
<p align="center">
  <img  height="500" src="https://imgur.com/vppVYwS.png">
  <img  height="500" src="https://imgur.com/eEQNweY.png">
  <img  height="500" src="https://imgur.com/MX1gAhR.png">
</p>

## How it works

Dark magic, Python 🐍, and the [python_telegram_bot](https://github.com/python-telegram-bot/python-telegram-bot) library.  
This bot allows potentially infinite players to play Boggle at the same time, while keeping the social distance required in these trying times.  

#### Some cool (🆒!) features:
- automatic word validation: if a word's not possible to make, the bot will tell you
- automatic detection for re-sent words and words that are too short
- integrated check for words in common with other players
- personal and group statistics  

This bot also has persistency, so that it can save all your stats to a database that will survive <i>at least</i> a restart (but I can't promise anything in case of a zombie apocalypse).

## How to play

You can find this bot at https://t.me/boggle_paroliere_bot. Add it to a group chat to play!

## How to host

If you want to run this bot on your own server, you need at least Python 3.6 and to follow these simple steps:
- `git clone https://github.com/e-caste/boggle-telegram-bot`
- `cd boggle-telegram-bot`
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `python boggle_telegram_bot.py`  
- When you're done: `deactivate` to exit the virtual environment where you've installed the requirements.

There is no noticeable improvement by using PyPy instead of CPython.
