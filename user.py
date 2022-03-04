from werkzeug.security import check_password_hash

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.password = password
        self.email    = email

    @staticmethod
    def is_authenitecated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymus():
        return False

    def get_id(self):
        return self.username

    def check_password(self, submited_password):
        return check_password_hash(self.password, submited_password)