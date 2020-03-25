from exceptions import LanguageNotFoundException, MessageNotFoundException

available_languages = ['ita', 'eng']

__group_welcome = {
    'ita': "🇮🇹 Ciao, e grazie per avermi aggiunto a questo gruppo! Sono Boggle/Paroliere Bot, e vi permetterò di "
           "giocare al Paroliere insieme!\n\n",
    'eng': "🇬🇧 Hi, thank you for adding me to this group! I am Boggle/Paroliere Bot, and I will allow you to play "
           "Boggle together!\n\n"
}

__usage = {
        'ita': "Per cambiare la lingua, i timer, o le dimensioni della tabella per "
               "questo gruppo, potete usare il comando /settings in questa chat.\n\nPrima di creare una partita, "
               "assicuratevi che tutti giocatori mi abbiano fatto partire <b>in una chat privata con me</b>: potete "
               "farlo scegliendo Avvia (o mandandomi"
               " il comando /start) dopo aver cliccato o toccato il mio nome.\nPer creare una partita usate /new, "
               "dopodiché tutti coloro che vorranno unirsi potranno usare /join. Se cambiate idea, potete lasciare la "
               "partita con /leave. Il creatore della partita può forzarne l'inizio col comando /startgame.\nA quel "
               "punto manderò a ciascuno dei giocatori un messaggio privato contenente la tabella coi dadi della "
               "partita, e prenderò nota di tutte le parole che mi manderete in privato.\nAllo scadere del tempo, "
               "manderò la lista delle parole che ciascuno di voi mi avrà mandato sulla chat di gruppo, e se stabilite "
               "che qualcuno ha inventato una parola (o mi ha mandato una parola non valida), il creatore della partita"
               " potrà cancellarla dalla sua lista con /delete 'parola/lista di parole' (senza ').\nLa partita "
               "termina quando il creatore della partita usa il comando /endgame.\n\nPotete dare un'occhiata agli altri"
               " miei comandi con /help.",
        'eng': "You can change the language, timers, and board dimensions for this group by using "
               "the /settings command in this chat.\n\nBefore creating a new game, make sure that all the people that "
               "want to play have started me <b>in a private chat with me</b>: you can do so by clicking or tapping on "
               "my name and choosing Start "
               "(or sending me the /start command).\nTo create a new game just use /new, then all the people who want "
               "to play can use /join. If something's come up or you've changed your mind, you can /leave the game. The"
               " game creator can force-start the game by using /startgame.\nAt that point I will send to each of the "
               "players a private message containing the board for the game, and I will take note of all the words "
               "you'll send me in private.\nAt the end of the timer, I will send the list of the words each of you will"
               " have sent to me to the group chat, and if you think someone has made up a word, the game creator can "
               "delete it from their list with /delete 'word/list of words' (without ').\nThe game ends when the "
               "game creator uses the /endgame command.\n\nYou can take a look at all my other commands with /help."
}

__rules = {
    'ita': "<b>Punteggi 4x4</b>\n"
           "1-2 lettere: 0 punti\n3-4 lettere: 1 punto\n5 lettere: 2 punti\n6 lettere: 3 punti\n7 lettere: 5 punti\n"
           "8+ lettere: 11 punti\n\n"
           "<b>Punteggi 5x5</b>\n"
           "1-2-3 lettere: 0 punti\n4 lettere: 1 punto\n5 lettere: 2 punti\n6 lettere: 3 punti\n7 lettere: 5 punti\n"
           "8+ lettere: 11 punti\n\n"
           "<b>Regole del gioco</b>\n"
           "Lo scopo del gioco è trovare il maggior numero possibile di parole nel tempo dato composte da lettere "
           "adiacenti sia ortogonalmente che diagonalmente. È vietato comporre una parola saltando una lettera o "
           "ripassando sullo stessa lettera.\nUna volta terminato il tempo a disposizione, i giocatori devono smettere "
           "di scrivere e sul gruppo verranno mandate le parole di ciascun giocatore: se una stessa parola è stata "
           "trovata da più giocatori, essa sarà stata cancellata dall'elenco. Se una parola è ritenuta non valida dagli"
           " altri giocatori, il creatore della partita può eliminarla con /delete 'parola/lista di parole'.\n\n"
           "<b>Validità delle parole</b>\n"
           "Sono ammesse le tipologie di parole determinate dal gruppo di giocatori. In generale, si possono usare le "
           "seguenti linee guida:\nsostantivi e aggettivi al maschile/femminile singolare/plurale, verbi all'infinito,"
           " avverbi, congiunzioni, interiezioni, onomatopee, preposizioni e pronomi sono sempre validi;\nverbi"
           " coniugati, sigle, parole straniere di uso comune in Italiano, nomi propri e geografici possono essere"
           " aggiunti per semplificare il gioco.",
    'eng': "<b>Scoring 4x4</b>\n"
           "1-2 letters: 0 points\n3-4 letters: 1 point\n5 letters: 2 points\n6 letters: 3 points\n7 letters: 5 points"
           "\n8+ letters: 11 points\n\n"
           "<b>Scoring 4x4</b>\n"
           "1-2-3 letters: 0 points\n4 letters: 1 point\n5 letters: 2 points\n6 letters: 3 points\n7 letters: 5 points"
           "\n8+ letters: 11 points\n\n"
           "<b>Rules of the game</b>\n"
           "The goal of the game is to find the maximum possible amount of words, made with adjacent letters both"
           " diagonally and vertically/horizontally, in the time given. It's forbidden to make a word skipping a letter"
           " or using the same letter more than once.\nOnce the time's finished, the players have to stop texting the "
           "bot, and it will send a message to the group chat containing the words of each player: if a word has been "
           "found by multiple players, it will have been removed from the list. If the players consider a word to be "
           "invalid, the game creator will be able to remove it from the player's list with /delete 'word/list of words"
           "'.\n\n"
           "<b>Word validity</b>\n"
           "The players can determine the allowed word categories. In general, you can use the following guidelines:\n"
           "nouns and adjectives, both masculine and feminine, both singular and plural, infinite verbs, adverbs, "
           "conjunctions, interjections, onomatopoeias, prepositions and pronouns are always valid;\n conjugated verbs,"
           " acronyms, foreign words of common use in English, first/last/geographical names can be allowed to simplify"
           " the game."
}

translations = {
    'welcome': {
        'ita': "Ciao <b>{}</b>, benvenuto/a su Boggle/Paroliere Bot!",
        'eng': "Hi <b>{}</b>, welcome to Boggle/Paroliere Bot!"
    },
    'bot_added_to_group': {
        'ita': __group_welcome['ita'] + __usage['ita'] + "\n\n\n" + __group_welcome['eng'] + __usage['eng'],
        'eng': __group_welcome['eng'] + __usage['eng'] + "\n\n\n" + __group_welcome['ita'] + __usage['ita']
    },
    'rules': {
        'ita': __rules['ita'],
        'eng': __rules['eng']
    },
    'usage': {
        'ita': __usage['ita'],
        'eng': __usage['eng']
    },
    'bot_not_started_by_user': {
        'ita': "Ehi, {}, non mi hai ancora avviato! Clicca o tocca il mio nome e premi Avvia o mandami il comando "
               "/start.",
        'eng': "Hey, {}, you haven't started me yet! Click or tap my name and select Start or send me the /start "
               "command."
    },
    'chat_is_not_group': {
        'ita': "Devi digitare questo comando in un gruppo! Aggiungimi a un gruppo con degli amici per giocare.",
        'eng': "You can only use this command in a group chat! Add me to a group with your friends to play."
    },
    'game_created': {
        'ita': "Nuova partita creata da {}! Potete entrare con /join entro {} secondi. /startgame per cominciare.\nIn "
               "partita:\n{}",
        'eng': "New game created by {}! You can now /join within {} seconds. /startgame to begin.\nJoined:\n{}"
    },
    'game_already_created': {
        'ita': "È già stata creata una partita! Puoi partecipare con /join.",
        'eng': "A game has already been created! You can still /join."
    },
    'game_already_started': {
        'ita': "La partita è già cominciata! Puoi creare la prossima partita con /new, o entrarci con /join, quando "
               "questa sarà finita.",
        'eng': "The game has already begun! When this game will end, you'll be able to create the next game with /new "
               "or /join in if someone else creates it before you."
    },
    'no_participants': {
        'ita': "Non ci sono giocatori! Usa /join per entrare in partita.",
        'eng': "There are no players! You can /join the game."
    },
    'game_joined': {
        'ita': "Okay, {}, sei in partita!",
        'eng': "Alright, {}, you're in!"
    },
    'game_left': {
        'ita': "Va bene, {}, sarà per un'altra volta.",
        'eng': "Okay, {}, we'll play another time."
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
    'not_in_game': {
        'ita': "{}, non sei nella partita in corso.",
        'eng': "{}, you're not in the current game."
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
        'ita': "La partita è cominciata! Giocate in chat privata!",
        'eng': "The game has begun! Let's play in the private chat!"
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
        'ita': "Questa parola è troppo corta!",
        'eng': "This word is too short!"
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
        'ita': "Tempo scaduto! Ecco il tuo punteggio:\n\n{}",
        'eng': "Time's up! Here's your score:\n\n{}"
    },
    'ingame_timer_expired_group': {
        'ita': "Tempo scaduto! Ora il creatore della partita ({}), in accordo con gli altri giocatori, dovrà mandarmi "
               "la lista delle parole non valide. Basta un messaggio con la lista delle parole non valide di tutti i "
               "giocatori, nella forma /delete 'lista di parole separate da spazi', ma accetto anche delle singole "
               "parole, se ricevo /delete 'parola' (sempre senza ').\n\n<b>Mi raccomando, {}, ricordati di "
               "darmi il comando /endgame per concludere la partita e visualizzare i risultati!</b>\n\nQui di seguito "
               "la lista complessiva:",
        'eng': "Time's up! Now the game creator ({}), in agreement with the other players, will have to send me the "
               "list of invalid words. A single message with the list of these words for all players in the form "
               "/delete 'list of space separated words' works, but I also accept messages for a single word like "
               "/delete 'word' (do not include ').\n\n<b>{}, please remember to send me the /endgame command to "
               "end the game and to see the results!</b>\n\nBelow you can find the list of words for each player:"
    },
    'game_not_yet_finished': {
        'ita': "Mi spiace, ma quel comando si può usare solo a partita finita.",
        'eng': "I'm sorry, but that command is only available after the game is finished."
    },
    'game_already_finished_kill': {
        'ita': "Non si può annullare una partita già terminata! Il creatore della partita, {}, deve usare /endgame per "
               "concludere la partita e visualizzare i punteggi.",
        'eng': "You can't kill a game that has already ended! The game, creator, {}, must use /endgame to end the game "
               "and show the scores."
    },
    'game_already_finished_kick': {
        'ita': "Non si può kickare un giocatore da una partita già terminata! Il creatore della partita, {}, deve usare"
               " /endgame per concludere la partita e visualizzare i punteggi.",
        'eng': "You can't kick a player from a game that has already ended! The game, creator, {}, must use /endgame to"
               " end the game and show the scores."
    },
    'game_already_finished_leave': {
        'ita': "Non puoi abbandonare una partita già terminata! Il creatore della partita, {}, deve usare"
               " /endgame per concludere la partita e visualizzare i punteggi.",
        'eng': "You can't leave a game that's already finished! The game, creator, {}, must use /endgame to"
               " end the game and show the scores."
    },
    'cant_kick_players_before_starting': {
        'ita': "Non puoi rimuovere dei giocatori dalla partita prima che cominci.",
        'eng': "You can't kick players from a game before it begins."
    },
    'char_not_alpha': {
        'ita': "Almeno un carattere nella parola '{}' non è disponibile tra quelli tra i dadi. Prova a correggerla e "
               "rimandami il messaggio.",
        'eng': "At least one character in the word '{}' is not available among the dice. Please resend me the message."
    },
    'words_not_found_in_players_words': {
        'ita': "Ho eliminato tutte le parole che mi hai mandato, fatta eccezione per queste: {}, perché non le ho "
               "trovate tra le parole segnate dai giocatori. Puoi riprovare a usare /delete 'lista di parole separate "
               "da spazi', o terminare la partita con /endgame.",
        'eng': "I've deleted all the words you've sent me, except these ones: {}, because I couldn't find them among "
               "the words sent me by the players. You can try again with /delete 'list of space separated words', or "
               "you can /endgame."
    },
    'all_words_deleted': {
        'ita': "Ho eliminato tutte le parole che mi hai mandato. Ora puoi mandarmi altre parole con /delete 'lista di "
               "parole separate da spazi', oppure terminare la partita con /endgame.",
        'eng': "I've deleted all the words you've sent me. Now you can either send me some other words with /delete '"
               "list of space separated words' or you can /endgame."
    },
    'no_words_after_delete_command': {
        'ita': "Il comando /delete da solo non basta, devi specificare quali parole vuoi cancellare.\nProva /delete "
               "'parola/lista di parole da cancellare' (senza ').",
        'eng': "The /delete command alone isn't enough, you have to specify which words you wish to delete.\nTry "
               "/delete 'word/list of words to delete' (without ')"
    },
    'game_finished': {
        'ita': "<b>Fine partita!</b>\n\n{}: {} con {} punti!",
        'eng': "<b>Game ended!</b>\n\n{}: {} with {} points!"
    },
    'game_winner_singular': {
        'ita': "E il vincitore è",
        'eng': "And the winner is"
    },
    'game_winners_plural': {
        'ita': "E i vincitori parimerito sono",
        'eng': "And the even winners are"
    },
    'game_killed_user_did_not_start_the_bot': {
        'ita': "La partita è stata annullata perché {} non mi ha avviato! Per farlo, entra nella chat privata con me e "
               "seleziona Avvia o mandami il comando /start.",
        'eng': "The game has been canceled because {} didn't start me! To do so, go to your private chat with me and "
               "select Start or send me the /start command."
    },
    'game_killed_group': {
        'ita': "La partita in corso è stata annullata! Per crearne una nuova, potete usare /new. Ricordatevi di usare "
               "/help se avete dei dubbi.",
        'eng': "The current game has been canceled! To create a new one, you can use /new. Remember to use /help if you"
               " have any doubts."
    },
    'game_killed_private': {
        'ita': "La partita a cui stavi giocando è stata annullata dal suo creatore, {}.",
        'eng': "The game you were playing has been canceled by its creator, {}."
    },
    'kick_user_choice_group': {
        'ita': "Il creatore della partita, {}, può scegliere chi kickare tra i giocatori:",
        'eng': "The game creator, {}, can choose who to kick from the game among the players:"
    },
    'no_users_to_kick': {
        'ita': "Non ci sono giocatori da rimuovere.",
        'eng': "No players to kick."
    },
    'forbid_kick_to_not_game_creator': {
        'ita': "Solo il creatore della partita può scegliere chi rimuovere!",
        'eng': "Only the game creator can choose who to kick!"
    },
    'kick_user_successful': {
        'ita': "Il giocatore {} è stato rimosso dalla partita corrente.",
        'eng': "The player {} has been kicked from the current game."
    },
    'you_have_been_kicked': {
        'ita': "Sei stato rimosso dalla partita da {}.",
        'eng': "You've been kicked from the game by {}."
    },
    'no_words_received': {
        'ita': "<i>Nessuna parola ricevuta.</i>",
        'eng': "<i>No words received.</i>"
    },
    'settings_prompt': {
        'ita': "Qui puoi cambiare le impostazioni per questo gruppo",
        'eng': "Here you can change the settings for this group chat"
    },
    'settings_button_language': {
        'ita': "Lingua",
        'eng': "Language"
    },
    'settings_button_timers': {
        'ita': "Timer",
        'eng': "Timers"
    },
    'settings_button_table_dimensions': {
        'ita': "Dimensioni tabella",
        'eng': "Board dimensions"
    },
    'settings_language_choice': {
        'ita': "Scegli la lingua:",
        'eng': "Choose your language:"
    },
    'settings_language_changed': {
        'ita': "Lingua cambiata!",
        'eng': "Language changed!"
    },
    'settings_timer_choice': {
        'ita': "Scegli quale timer vuoi cambiare:",
        'eng': "Choose which timer you want to change:"
    },
    'settings_newgame_timer_button': {
        'ita': "Tempo del pre-partita",
        'eng': "Pre-game duration"
    },
    'settings_ingame_timer_button': {
        'ita': "Tempo della partita",
        'eng': "Game duration"
    },
    'settings_newgametimer_changed': {
        'ita': "Durata del pre-partita cambiata!",
        'eng': "Pre-game duration changed!"
    },
    'settings_ingametimer_changed': {
        'ita': "Durata della partita cambiata!",
        'eng': "Game duration changed!"
    },
    'settings_board_choice': {
        'ita': "Scegli la dimensione della tabella:",
        'eng': "Choose the board dimensions:"
    },
    'settings_board_changed': {
        'ita': "Dimensioni della tabella cambiate in {}!",
        'eng': "Board dimensions changed to {}!"
    },
    'stats_prompt': {
        'ita': "Che statistiche vuoi vedere?",
        'eng': "Which stats do you want to check out?"
    },
    'stats_user_button': {
        'ita': "Le mie statistiche",
        'eng': "My stats"
    },
    'stats_group_button': {
        'ita': "Le statistiche del gruppo",
        'eng': "Group stats"
    },
    'stats_shown_below': {
        'ita': "Ecco le statistiche:",
        'eng': "Here are your stats:"
    },
    'stats_group_matches': {
        'ita': "Numero di partite:",
        'eng': "Number of games:"
    },
    'stats_group_points': {
        'ita': "Punti totali di questo gruppo:",
        'eng': "Total points of this group:"
    },
    'stats_group_average': {
        'ita': "Media di punti per partita:",
        'eng': "Average points per game:"
    },
    'stats_user_matches': {
        'ita': "Partite",
        'eng': "Games"
    },
    'stats_user_won_matches': {
        'ita': "Vinte:",
        'eng': "Won:"
    },
    'stats_user_even_matches': {
        'ita': "Vittorie parimerito:",
        'eng': "Even:"
    },
    'stats_user_lost_matches': {
        'ita': "Perse:",
        'eng': "Lost:"
    },
    'stats_user_total_matches': {
        'ita': "Giocate:",
        'eng': "Played:"
    },
    'stats_user_points': {
        'ita': "Punteggio",
        'eng': "Points"
    },
    'stats_user_max_points': {
        'ita': "Massimo:",
        'eng': "Maximum"
    },
    'stats_user_min_points': {
        'ita': "Minimo:",
        'eng': "Minimum:"
    },
    'stats_user_average_points': {
        'ita': "Medio:",
        'eng': "Average"
    },
    'stats_user_total_points' : {
        'ita': "Totali:",
        'eng': "Total:"
    },
    'stats_user_latest_game': {
        'ita': "Ultima partita",
        'eng': "Latest game"
    },
    'stats_user_latest_game_points': {
        'ita': "Punteggio:",
        'eng': "Points:"
    },
    'stats_user_latest_game_words': {
        'ita': "Parole:",
        'eng': "Words:"
    },
    'game_canceled_because_bot_restarted': {
        'ita': "Mi spiace, ma la partita a cui stavate giocando è stata annullata perché sono stato riavviato e (d'oh!)"
               " ho perso il timer, quindi non avrei saputo dirvi quando sarebbe terminata.\nPotete creare una nuova "
               "partita con /new!",
        'eng': "I'm sorry, but the game you were playing has been canceled because I've been restarted and (d'oh!) I've"
               " lost my timer, so I wouldn't have been able to tell you when it should have ended.\nYou can still "
               "create a /new game!"
    },
    'help': {
        'ita': "Usa /start per far partire il bot in una chat privata.\n"
               "Usa /new per cominciare una partita del Paroliere in un gruppo.\n"
               "Usa /join per entrare in una partita. Puoi uscire con /leave se cambi idea.\n"
               "Usa /startgame per far cominciare una partita che hai creato.\n"
               "Usa /delete 'lista di parole separate da spazi' per eliminare delle parole non valide da quelle che mi "
               "hanno mandato i giocatori.\n"
               "Usa /endgame per far terminare una partita che hai creato e vedere chi ha vinto.\n"
               "Usa /kick per far uscire qualcuno da una partita che hai creato.\n"
               "Usa /kill per annullare una partita che hai creato.\n"
               "Usa /stats per dare un'occhiata alle tue statistiche o a quelle del gruppo.\n"
               "Usa /settings per modificare le impostazioni per te o per un gruppo.\n"
               "Usa /rules per visualizzare le regole del Paroliere.\n"
               "Usa /usage per visualizzare come utilizzare il bot più in dettaglio.\n"
               "Usa /help per mostrare questo messaggio.",
        'eng': "Use /start to start the bot in a private chat.\n"
               "Use /new to create a new Boggle game in a group.\n"
               "Use /join to join a game.\n"
               "Use /startgame to start a game you've created.\n"
               "Use /delete 'list of space-separated words' to delete the invalid words sent by the players.\n"
               "Use /endgame to end a game you've created.\n"
               "Use /kick to remove a player from a game you've created.\n"
               "Use /kill to cancel a game you've created.\n"
               "Use /stats to check your statistics.\n"
               "Use /settings to change settings for you or for a group.\n"
               "Use /rules to show the rules of Boggle.\n"
               "Use /usage to show a more detailed message on how to use the bot.\n"
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
