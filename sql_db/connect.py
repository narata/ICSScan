import MySQLdb

host = 'localhost'
user = 'root'
passwd = 'narata'
db = 'hammer'
port = 3306


def connect_db():
    try:
        con = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, port=port)
        return con
    except MySQLdb.Error:
        return False