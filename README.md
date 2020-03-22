# boggle-telegram-bot

<p align="center">
  <img  height="600" src="https://imgur.com/vppVYwS.png">
  <img  height="600" src="https://imgur.com/FCCSec6.png">
</p>

## How it works

Dark magic, Python 🐍, and the [python_telegram_bot](https://github.com/python-telegram-bot/python-telegram-bot) library.  
It allows potentially infinite players to play Boggle at the same time, while keeping the social distance required in these trying times.  

This bot also has persistency, so that it can save all your stats to a database that will survive <i>at least</i> a restart (but I can't promise anything in case of a zombie apocalypse).

## How to play

You can find this bot at https://t.me/boggle_paroliere_bot. Add it to a group chat to play!

## How to run

If you want to run this bot on your own server, you need at least Python 3.6 and to follow these simple steps:
- `git clone https://github.com/e-caste/boggle-telegram-bot`
- `cd boggle-telegram-bot`
- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `python boggle_telegram_bot.py`  
- When you're done: `deactivate` to exit the virtual environment where you've installed the requirements.
