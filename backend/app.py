import datetime
from flask import Flask, jsonify,Flask, request
from backend.database_operations.mysql_credentials_reader import MysqlCredentials
from backend.database_operations.mysql_connection import DatabaseConnection
from backend.database_operations.user import UserDAO, UserLogin, UserRegistration

app = Flask(__name__)
db_name = 'ai_trainer'
credentials =  MysqlCredentials.get_mysql_credentials()
connection = DatabaseConnection.connect_to_mysql_server(credentials['DBN'],credentials['mysql_username'],credentials['mysql_pwd'],credentials['mysql_host'])
user_login = UserLogin(connection, db_name)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)