
from backend.database_operations.mysql_credentials_reader import  MysqlCredentials
import json
import pymysql
class DatabaseConnection :
    def __init__(self):
        pass
    
    def connect_to_mysql_server(self,DBUSERNAME,PWD,hostname,):
        client = pymysql.connect(host=hostname, user=DBUSERNAME, password=PWD, )
        return client
    
   
# database_connection().connect_to_mysql_server
# for testing daatabase connection

# mysql_credentials = MysqlCredentials.get_mysql_credentials()
# DatabaseConnection().connect_to_mysql_server(mysql_credentials['mysql_username'],mysql_credentials['mysql_pwd'],mysql_credentials['mysql_host'])

