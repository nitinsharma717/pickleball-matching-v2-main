# exceptions.py
class PlayerInfoException(Exception):
    ...


class PlayerInfoNotFoundError(PlayerInfoException):
    def __init__(self):
        self.status_code = 404
        self.detail = "Player Info Not Found"

class PlayerInfoInvalid(PlayerInfoException):
    def __init__(self):
        self.status_code = 422
        self.detail = "Player Info Invalid"

class EmailInvalid(PlayerInfoException):
    def __init__(self):
        self.status_code = 422
        self.detail = "Email Invalid"


class PlayerInfoInfoAlreadyExistError(PlayerInfoException):
    def __init__(self):
        self.status_code = 409
        self.detail = "Player Info Already Exists"
