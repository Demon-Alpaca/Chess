import mysql.connector
from mysql.connector import errorcode


# config = {
#     'user': 'root',
#     'password': '12345',
#     'host': 'localhost',
#     'database': 'db_chess'
# }

class ConnectSql(object):
    """docstring for ConnectSql"""
    def __init__(self, config):
        super(ConnectSql, self).__init__()
        self.config = config
        self.cnx = None

    # 链接数据库
    def connect(self):
        try:
            cnx = mysql.connector.connect(**self.config)
            self.cnx = cnx
            print("Connect Success")
            return cnx
        except mysql.connector.Error as err:
            # 用户名或密码错误
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("username password error")
            # 数据库不存在
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print('DB not exist')
            else:
                print(err)

    # 关闭数据库链接
    def close(self):
        self.cnx.close()
