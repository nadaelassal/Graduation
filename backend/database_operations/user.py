import crypt
from hashlib import scrypt
import bcrypt
class User:
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

 