import crypt
from hashlib import scrypt
import bcrypt
class User:
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

 
class UserDAO:
    def __init__(self, connection, db_name):
        self.connection = connection
        self.db_name = db_name

    def retrieve_user_information(self, email):
        cur = self.connection.cursor()
        cur.execute(
            f"SELECT * FROM {self.db_name}.user_info where (email = %s)",
            (email.lower(),))
        user_information = cur.fetchone()
        if user_information:
            columns = [col[0] for col in cur.description]
            user_dict = dict(zip(columns, user_information))
            return user_dict
        else:
            return None

    def execute_query(self, query, *params):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchone()
            return result

    def insert_user(self, user):
        query = f"INSERT INTO {self.db_name}.user_info (email, username, password) VALUES (%s, %s, %s)"
        self.execute_query(query, user.email.lower(), user.username.lower(), user.password)
        self.connection.commit()
    
    def update_password(self, email, new_password):
        query = f"UPDATE {self.db_name}.user_info SET password = %s WHERE email = %s"
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.execute_query(query, hashed_password, email.lower())
        self.connection.commit()    
    def update_user_information(self, email, height, weight, age):
        query = f"UPDATE {self.db_name}.user_info SET height = %s, weight = %s, age = %s WHERE email = %s"
        self.execute_query(query, height, weight, age, email.lower())
        return self.connection.commit()
        
        
