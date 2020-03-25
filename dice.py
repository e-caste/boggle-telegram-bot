from random import shuffle, choice
from exceptions import LanguageNotFoundException, TableDimensionsNotFoundException

dice = {
    'ita': {
        '4x4': [
            ["L", "E", "P", "U", "S", "T"],
            ["O", "E", "U", "N", "C", "T"],
            ["O", "Qu", "A", "M", "O", "B"],
            ["R", "I", "F", "O", "A", "C"],
            ["O", "S", "A", "I", "M", "R"],
            ["V", "I", "T", "E", "N", "G"],
            ["E", "R", "A", "L", "S", "C"],
            ["L", "R", "O", "E", "I", "U"],
            ["A", "M", "E", "D", "C", "P"],
            ["D", "A", "N", "E", "Z", "V"],
            ["I", "R", "E", "N", "H", "S"],
            ["T", "E", "S", "O", "N", "D"],
            ["T", "L", "R", "B", "I", "A"],
            ["E", "E", "I", "S", "H", "F"],
            ["O", "I", "A", "A", "T", "E"],
            ["N", "U", "L", "E", "G", "O"]
        ],
        '5x5': [
            ["A", "A", "E", "I", "O", "T"],
            ["A", "B", "I", "L", "R", "T"],
            ["A", "B", "M", "O", "O", "Qu"],
            ["A", "C", "D", "E", "M", "P"],
            ["A", "C", "E", "L", "R", "S"],
            ["A", "C", "F", "I", "O", "R"],
            ["A", "D", "E", "N", "V", "Z"],
            ["A", "I", "M", "O", "R", "S"],
            ["C", "E", "N", "O", "T", "U"],
            ["D", "E", "N", "O", "S", "T"],
            ["E", "E", "F", "H", "I", "S"],
            ["E", "G", "I", "N", "T", "V"],
            ["E", "G", "L", "N", "O", "U"],
            ["E", "H", "I", "N", "R", "S"],
            ["E", "I", "L", "O", "R", "U"],
            ["E", "L", "P", "S", "T", "U"],
            ["A", "B", "C", "I", "M", "O"],
            ["A", "B", "F", "Qu", "S", "Z"],
            ["A", "C", "G", "I", "P", "T"],
            ["A", "C", "G", "P", "S", "V"],
            ["A", "F", "G", "I", "P", "R"],
            ["B", "E", "L", "F", "N", "O"],
            ["C", "D", "I", "L", "M", "O"],
            ["C", "I", "L", "M", "O", "R"],
            ["D", "I", "M", "O", "T", "V"]
        ]
    },
    'eng': {
        '4x4': [
            ["L", "R", "Y", "T", "T", "E"],
            ["V", "T", "H", "R", "W", "E"],
            ["E", "G", "H", "W", "N", "E"],
            ["S", "E", "O", "T", "I", "S"],
            ["A", "N", "A", "E", "E", "G"],
            ["I", "D", "S", "Y", "T", "T"],
            ["O", "A", "T", "T", "O", "W"],
            ["M", "T", "O", "I", "C", "U"],
            ["A", "F", "P", "K", "F", "S"],
            ["X", "L", "D", "E", "R", "I"],
            ["H", "C", "P", "O", "A", "S"],
            ["E", "N", "S", "I", "E", "U"],
            ["Y", "L", "D", "E", "V", "R"],
            ["Z", "N", "R", "N", "H", "L"],
            ["N", "M", "I", "Qu", "H", "U"],
            ["O", "B", "B", "A", "O", "J"]
        ]
    }
}

letters_sets = {
    'ita': set('abcdefghilmnopqrstuvz'),
    'eng': set('abcdefghijklmnopqrstuvwxyz')
}


def get_shuffled_dice(lang: str, table_dimensions: str) -> list:
    if lang not in dice:
        raise LanguageNotFoundException(f"Language {lang} is not available for translation.")
    if table_dimensions not in dice[lang]:
        raise TableDimensionsNotFoundException(f"The table dimensions {table_dimensions} "
                                               f"are not available for the language {lang}.")

    tmp = dice[lang][table_dimensions].copy()
    shuffle(tmp)
    for i, die in enumerate(tmp):
        tmp[i] = choice(die)

    return tmp


if __name__ == '__main__':
    print(get_shuffled_dice('eng', '4x4'))
