class LanguageNotFoundException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class TableDimensionsNotFoundException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class MessageNotFoundException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
