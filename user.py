from werkzeug.security import check_password_hash
from flask_login import UserMixin, AnonymousUserMixin

class User():
    def __init__(self, username, email, password):
        self.username = username
        self.password = password
        self.email    = email

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymus(self):
        return False

    def get_id(self):
        return self.username

    def check_password(self, submited_password):
        return check_password_hash(self.password, submited_password)