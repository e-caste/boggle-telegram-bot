from exceptions import LanguageNotFoundException


def get_string(lang: str, msg: str, *args) -> str:
    if lang in available_languages:
        return translations[msg][lang].format(args)
    else:
        raise LanguageNotFoundException(f"Language {lang} is not available for translation.")


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


if __name__ == '__main__':
    print(get_string('ita', 'welcome', 'Mario'),
          "\n",
          get_string('eng', 'welcome', 'Mark'))
