from exceptions import LanguageNotFoundException, MessageNotFoundException

available_languages = ['ita', 'eng']

translations = {
    'welcome': {
        'ita': "Ciao <b>{}</b>, benvenuto/a su Boggle/Paroliere Bot!",
        'eng': "Hi <b>{}</b>, welcome to Boggle/Paroliere Bot!"
    },
    'chat_is_not_group': {
        'ita': "Devi digitare questo comando in un gruppo! Aggiungimi a un gruppo con degli amici per giocare.",
        'eng': "You can only use this command in a group chat! Add me to a group with your friends to play."
    },
    'game_created': {
        'ita': "Nuova partita creata da {}! Potete entrare con /join entro {} secondi.",
        'eng': "New game created by {}! You can now /join within {} seconds."
    },
    'game_already_created': {
        'ita': "È già stata creata una partita! Puoi partecipare con /join.",
        'eng': "A game has already been created! You can still /join."
    },
    'game_joined': {
        'ita': "Okay, {}, sei in partita!",
        'eng': "Alright, {}, you're in!"
    },
    'game_left': {
        'ita': "Va bene, {}, sarà per un'altra volta. Usa /join se vuoi rientrare in partita.",
        'eng': "Okay, {}, we'll play another time. Use /join if you change your mind."
    },
    'already_in_game': {
        'ita': "Hey {}, sei già in una partita! Il creatore della partita, {}, può farla cominciare col comando "
               "/startgame.",
        'eng': "Hey {}, you've already joined a game! The game creator, {}, can start it with /startgame."
    },
    'not_yet_in_game': {
        'ita': "{}, non sei ancora entrato in partita! Usa /join per entrare.",
        'eng': "{}, you're not in a game yet! You can /join the current game if you want."
    },
    'no_game_yet': {
        'ita': "Non è ancora stata creata nessuna partita. Puoi crearne una con /new.",
        'eng': "No game has been created yet. You can create one with /new."
    },
    'newgame_timer_expired': {
        'ita': "Tempo scaduto. La parita è stata cancellata, dato che nessun giocatore è entrato. Potete creare una "
               "nuova partita con /new.",
        'eng': "Timer expired. The game was canceled since no player joined. You can create a new game with /new."
    },
    'forbid_not_game_creator': {
        'ita': "Mi spiace, {}, ma solo il creatore della partita ({}) può usare {}.",
        'eng': "Sorry, {}, but only the game creator ({}) can use {}."
    },
    'game_started_group': {
        'ita': "La partita è cominciata! Ho inviato a ciascuno dei partecipanti un messaggio in chat privata, lì "
               "dovrete scrivermi tutte le parole che riuscite a trovare tra i dadi! Che vinca il migliore!",
        'eng': "The game has begun! I've sent a message to each of the partecipants in their private chat, and that's "
               "where you'll have to send me all of the words you can find among the dice! May the best player win!"
    },
    'game_started_private': {
        'ita': "Qui puoi mandarmi tutte le parole che trovi nella tabella seguente. Presto che è tardi, hai solo {} "
               "secondi!",
        'eng': "Here you can send me all the words you can find in the table below. Quick, you only have {} seconds!"
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
