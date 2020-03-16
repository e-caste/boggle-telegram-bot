from exceptions import LanguageNotFoundException, MessageNotFoundException

available_languages = ['ita', 'eng']

translations = {
    'welcome': {
        'ita': "Ciao <b>{}</b>, benvenuto/a su Boggle/Paroliere Bot!",
        'eng': "Hi <b>{}</b>, welcome to Boggle/Paroliere Bot!"
    },
    'chat_is_not_group': {
        'ita': "Devi digitare questo comando in un gruppo!",
        'eng': "You can only use this command in a group chat!"
    },
    'game_created': {
        'ita': "Nuova partita creata da {}! Potete entrare con /join",
        'eng': "New game created by {}! You can now /join"
    },
    'game_already_started': {
        'ita': "È già stata creata una partita! Puoi partecipare con /join",
        'eng': "A game has already been created! You can still /join"
    },
    'game_joined': {
        'ita': "Okay, {}, sei in partita!",
        'eng': "Alright, {}, you're in!"
    },
    'no_game_yet': {
        'ita': "Non è ancora stata creata nessuna partita. Puoi crearne una con /new",
        'eng': "No game has been created yet. You can create one with /new"
    },
    'help': {
        'ita': "Usa /start per far partire il bot.\n"
               "Usa /new per cominciare una partita del Paroliere in un gruppo.\n"
               "Usa /stats per dare un'occhiata alle tue statistiche.\n"
               "Usa /help per mostrare questo messaggio.",
        'eng': "Use /start to start the bot.\n"
               "Use /new to begin a new Boggle game in a group.\n"
               "Use /stats to check your statistics.\n"
               "Use /help to show this help."
    }
}


def get_string(lang: str, msg: str, *args) -> str:
    if lang not in available_languages:
        raise LanguageNotFoundException(f"Language {lang} is not available for translation.")
    elif msg not in translations:
        raise MessageNotFoundException(f"Message {msg} is not available.")
    else:
        return translations[msg][lang].format(*args)


if __name__ == '__main__':
    print(get_string('ita', 'welcome', 'Mario'),
          "\n",
          get_string('eng', 'welcome', 'Mark'))
