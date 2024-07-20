import mysql.connector
from api.config.mysql import MYSQL_CONFIG

def connect_db():
    return mysql.connector.connect(
        host = MYSQL_CONFIG['host'],
        user = MYSQL_CONFIG['user'],
        password = MYSQL_CONFIG['password'],
        database = MYSQL_CONFIG['database']
    )
