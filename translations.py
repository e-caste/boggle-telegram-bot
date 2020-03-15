class LanguageNotFoundException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


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
    }
}


if __name__ == '__main__':
    print(get_string('ita', 'welcome', 'Mario'),
          "\n",
          get_string('eng', 'welcome', 'Mark'))
