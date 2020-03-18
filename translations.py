from exceptions import LanguageNotFoundException, MessageNotFoundException

available_languages = ['ita', 'eng']

translations = {
    'welcome': {
        'ita': "Ciao <b>{}</b>, benvenuto/a su Boggle/Paroliere Bot!",
        'eng': "Hi <b>{}</b>, welcome to Boggle/Paroliere Bot!"
    },
    'bot_added_to_group': {
        'ita': "🇬🇧 Hi, thank you for adding me to this group! I am Boggle/Paroliere Bot, and I will allow you to play "
               "Boggle together!\n\nYou can change the language, timers, and board dimensions for this group by using "
               "the /settings command in this chat.\n\nBefore creating a new game, make sure that all the people that "
               "want to play have started me: you can do so by clicking or tapping on my name and choosing Start "
               "(or sending the /start command).\nTo create a new game just use /new, then all the people who want to "
               "play can use /join. If something's come up or you've changed your mind, you can /leave the game. The "
               "game creator can force-start the game by using /startgame.\nAt that point I will send to each of the "
               "players a private message containing the board for the game, and I will take note of all the words "
               "you'll send me in private.\nAt the end of the timer, I will send the list of the words each of you will"
               " have sent to me to the group chat, and if you think someone has made up a word, the game creator can "
               "delete it from their list with /delete <word/list of words> (without < and >).\nThe game ends when the "
               "game creator uses the /endgame command.\n\nYou can take a look at all my other commands with /help."
               "\n\n\n"
               "🇮🇹 Ciao, e grazie per avermi aggiunto a questo gruppo! Sono Boggle/Paroliere Bot, e vi permetterò di "
               "giocare al Paroliere insieme!\n\nPer cambiare la lingua, i timer, o le dimensioni della tabella per "
               "questo gruppo, potete usare il comando /settings in questa chat.\n\nPrima di creare una partita, "
               "assicuratevi che tutti giocatori mi abbiano fatto partire: potete farlo scegliendo Start (o mandandomi"
               " il comando /start) dopo aver cliccato o toccato il mio nome.\nPer creare una partita usate /new, "
               "dopodiché tutti coloro che vorranno unirsi potranno usare /join. Se cambiate idea, potete lasciare la "
               "partita con /leave. Il creatore della partita può forzarne l'inizio col comando /startgame.\nA quel "
               "punto manderò a ciascuno dei giocatori un messaggio privato contenente la tabella coi dadi della "
               "partita, e prenderò nota di tutte le parole che mi manderete in privato.\nAllo scadere del tempo, "
               "manderò la lista delle parole che ciascuno di voi mi avrà mandato sulla chat di gruppo, e se stabilite "
               "che qualcuno ha inventato una parola (o mi ha mandato una parola non valida), il creatore della partita"
               " potrà cancellarla dalla sua lista con /delete <parola/lista di parole> (senza < e >).\nLa partita "
               "termina quando il creatore della partita usa il comando /endgame.\n\nPotete dare un'occhiata agli altri"
               " miei comandi con /help.",
        'eng': "🇬🇧 Hi, thank you for adding me to this group! I am Boggle/Paroliere Bot, and I will allow you to play "
               "Boggle together!\n\nYou can change the language, timers, and board dimensions for this group by using "
               "the /settings command in this chat.\n\nBefore creating a new game, make sure that all the people that "
               "want to play have started me: you can do so by clicking or tapping on my name and choosing Start "
               "(or sending the /start command).\nTo create a new game just use /new, then all the people who want to "
               "play can use /join. If something's come up or you've changed your mind, you can /leave the game. The "
               "game creator can force-start the game by using /startgame.\nAt that point I will send to each of the "
               "players a private message containing the board for the game, and I will take note of all the words "
               "you'll send me in private.\nAt the end of the timer, I will send the list of the words each of you will"
               " have sent to me to the group chat, and if you think someone has made up a word, the game creator can "
               "delete it from their list with /delete <word/list of words> (without < and >).\nThe game ends when the "
               "game creator uses the /endgame command.\n\nYou can take a look at all my other commands with /help."
               "\n\n\n"
               "🇮🇹 Ciao, e grazie per avermi aggiunto a questo gruppo! Sono Boggle/Paroliere Bot, e vi permetterò di "
               "giocare al Paroliere insieme!\n\nPer cambiare la lingua, i timer, o le dimensioni della tabella per "
               "questo gruppo, potete usare il comando /settings in questa chat.\n\nPrima di creare una partita, "
               "assicuratevi che tutti giocatori mi abbiano fatto partire: potete farlo scegliendo Start (o mandandomi"
               " il comando /start) dopo aver cliccato o toccato il mio nome.\nPer creare una partita usate /new, "
               "dopodiché tutti coloro che vorranno unirsi potranno usare /join. Se cambiate idea, potete lasciare la "
               "partita con /leave. Il creatore della partita può forzarne l'inizio col comando /startgame.\nA quel "
               "punto manderò a ciascuno dei giocatori un messaggio privato contenente la tabella coi dadi della "
               "partita, e prenderò nota di tutte le parole che mi manderete in privato.\nAllo scadere del tempo, "
               "manderò la lista delle parole che ciascuno di voi mi avrà mandato sulla chat di gruppo, e se stabilite "
               "che qualcuno ha inventato una parola (o mi ha mandato una parola non valida), il creatore della partita"
               " potrà cancellarla dalla sua lista con /delete <parola/lista di parole> (senza < e >).\nLa partita "
               "termina quando il creatore della partita usa il comando /endgame.\n\nPotete dare un'occhiata agli altri"
               " miei comandi con /help."
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
        'ita': "Okay, {}, sei in partita! Il creatore della partita, {}, può farla cominciare con /startgame.",
        'eng': "Alright, {}, you're in! The game creator, {}, can start it with /startgame."
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
    'received_dm_but_user_not_in_game': {
        'ita': "Ehi, mi hai scritto ma non sei in nessuna partita! Puoi aggiungermi a un gruppo con degli amici e usare"
               " lì il comando /new per crearne una.",
        'eng': "Hey, you texted me but you're not in any game at the moment! You can add me to a group with your "
               "friends and use the /new command there to create one."
    },
    'received_dm_but_char_not_alpha': {
        'ita': "Ehi, sembra che questo messaggio contenga dei caratteri non presenti tra i dadi, l'ho scartato.",
        'eng': "Hey, it looks like this message contains some characters which can't be found on the dice, "
               "I've discarded it."
    },
    'received_dm_but_word_too_short': {
        'ita': "Questa parola è troppo corta: nel Paroliere le parole devono essere lunghe almeno 3 lettere.",
        'eng': "This word is too short: in Boggle, words must be at least 3 letters long."
    },
    'received_dm_but_word_not_validated': {
        'ita': "Ehi, hai digitato una parola impossibile da comporre con queste lettere, quindi l'ho scartata.",
        'eng': "Hey, you've sent me an impossible word to make using these letters, so I've discarded it."
    },
    'received_dm_but_q_without_u': {
        'ita': "Non puoi usare la lettera Q senza che sia seguita da una U! Ho scartato la parola.",
        'eng': "You can't use the letter Q without it being followed by U! I've discarded your last word."
    },
    'received_dm_but_word_already_sent': {
        'ita': "Mi hai già mandato la parola '{}' in questa partita.",
        'eng': "You've already sent me the word '{}' during this game."
    },
    'ingame_timer_expired_private': {
        'ita': "Tempo scaduto! Ecco il tuo punteggio: {}",
        'eng': "Time's up! Here's your score: {}"
    },
    'ingame_timer_expired_group': {
        'ita': "Tempo scaduto! Ora il creatore della partita ({}), in accordo con gli altri giocatori, dovrà mandarmi "
               "la lista delle parole non valide. Basta un messaggio con la lista delle parole non valide di tutti i "
               "giocatori, nella forma /delete <lista di parole separate da spazi>, ma accetto anche delle singole "
               "parole, se ricevo /delete <parola> (sempre senza < né >).\n\n<b>Mi raccomando, {}, ricordati di "
               "darmi il comando /endgame per concludere la partita e visualizzare i risultati!</b>\n\nQui di seguito "
               "la lista complessiva:\n\n{}",
        'eng': "Time's up! Now the game creator ({}), in agreement with the other players, will have to send me the "
               "list of invalid words. A single message with the list of these words for all players in the form "
               "/delete <list of space separated words> works, but I also accept messages for a single word like "
               "/delete <word> (do not include < and >).\n\n<b>{}, please remember to send me the /endgame command to "
               "end the game and to see the results!</b>\n\nBelow you can find the list of words for each player:\n\n{}"
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
