import bcrypt
from hashlib import scrypt

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

class UserRegistration:
    def __init__(self,connection,DBN):
        self.user_dao = UserDAO(connection,DBN)

    def register_user(self, email, username, password):
        # Check if username is already taken
        user_info = self.user_dao.retrieve_user_information(email)
        if user_info is not None:
            print(f"email '{email}' is already taken")
            return False

        # Hash the password using a secure algorithm
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Create a User object with the provided information
        user = User(email=email, username=username, password=hashed_password)

        # Insert the user information into the database using the UserDAO object
        self.user_dao.insert_user(user)

        print(f"email '{email}' has been registered successfully")
        return True

class UserLogin:
    def __init__(self, connection,DBN):
        self.user_dao = UserDAO(connection,DBN)

    def authenticate_user(self, email, password):
        # Retrieve user information from the database based on the username
        user_info = self.user_dao.retrieve_user_information(email)
        
        if user_info is None:
            print(f"email '{email}' does not exist")
            return False

        # Check if the provided password matches the stored hash
        hashed_password = user_info['password']
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            print(f"User '{email}' has been authenticated successfully")
            return True
       

    def reset_password(self, email, new_password):
        user_info = self.user_dao.retrieve_user_information(email)
        
        if user_info is None:
            print(f"email '{email}' does not exist")
            return False

        self.user_dao.update_password(email, new_password)
        print(f"Password for user '{email}' has been updated successfully")
        return True

    