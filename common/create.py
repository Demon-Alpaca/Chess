import mysql.connector
from mysql.connector import errorcode
from common.connect import ConnectSql


def create_database(cursor, DB_NAME):
    try:
        cursor.execute("CREATE DATABASE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("create database failed : {}".format(err))
        exit(1)


class MysqlWork(object):

    """cnx store the connection object cursor is the MySQLCursor object_"""
    def __init__(self, config=None):
        super(MysqlWork, self).__init__()
        self.config = config
        self.cnx = None
        self.cursor = None

    def connect(self, config=None):
        if config is None:
            connectSql = ConnectSql(self.config)
            self.cnx = connectSql.connect()
            self.cursor = self.cnx.cursor()
        else:
            connectSql = ConnectSql(config)
            self.cnx = connectSql.connect()
            self.cursor = self.cnx.cursor()

    def close(self):
        self.cursor.close()
        self.cnx.close()
        print("Closed Mysql, Bye Bye!!!")

    def create_database(self, DB_NAME):
        create_database(self.cursor, DB_NAME)

    def create_table(self, DB_NAME, TABLES):
        try:
            self.cursor.execute("USE {}".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Database ** {} ** does not exit".format(DB_NAME))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                # 如果不存在则创建 数据库
                create_database(self.cursor, DB_NAME)
                print("Database ** {} ** created successfully".format(DB_NAME))
                self.cnx.database = DB_NAME
            else:
                print(err)
                exit(1)
        # 创建表
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table ** {} ** : ".format(table_name), end='')
                self.cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    # 如果该表已经存在 返回-1
                    return -1
            else:
                print('ok')

    def delete_table(self, DB_NAME, TB_NAME):
        try:
            self.cursor.execute("USE {}".format(DB_NAME))
        except mysql.connector.Error as err:
            print("Database {} does not exit".format(DB_NAME))
            print(err)
            exit(1)
        try:
            self.cursor.execute("DROP TABLE {}".format(TB_NAME))
            print("delete table ** {} ** successfully".format(TB_NAME))
        except mysql.connector.Error as err:
            print("delete table ** {} ** failed : {}".format(TB_NAME, err))
            exit(1)

    def insert_data(self, DB_NAME, sql, data):
        # sql是sql语句 data是要插入的数据 格式为元组
        # 指定数据库
        try:
            self.cursor.execute("USE {}".format(DB_NAME))
        except mysql.connector.Error as err:
            # 数据库不存在
            print("Database {} does not exit".format(DB_NAME))
            print(err)
            exit(1)
        self.cursor.execute(sql, data)
        self.cnx.commit()
        print("Insert into tabel ** {} ** successfully".format(DB_NAME))

    def query_data(self, DB_NAME, sql, data=None):
        try:
            self.cursor.execute("USE {}".format(DB_NAME))
        except mysql.connector.Error as err:
            # 数据库不存在
            print("Database {} does not exit".format(DB_NAME))
            print(err)
            exit(1)
        self.cursor.execute(sql, data)
        return self.cursor
        print("Query_data into tabel ** {} ** successfully".format(DB_NAME))
