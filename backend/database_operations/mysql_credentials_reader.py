import json
class MysqlCredentials:
    @staticmethod 
    def get_mysql_credentials():
        with open('backend/database_operations/mysql_credentials.json', 'r') as f:
            data = json.load(f)
        return data