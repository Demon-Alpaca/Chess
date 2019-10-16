from create import MysqlWork


def test_mysql_create():
    config = {
        'user': 'root',
        'password': '12345',
        'host': 'localhost',
    }

    DB_NAME = 'db_chess'
    TB_NAME = 'tb_chess'

    TABLES = {}
    TABLES['tb_chess'] = (
            "CREATE TABLE `tb_chess`("
            "`count` bigint(226),"
            "`x` varchar(2),"
            "`y` varchar(2),"
            "`color` int(3),"
            "PRIMARY KEY (`count`)"
            ") ENGINE=InnoDB"
        )
    mysqlWork = MysqlWork(config)
    mysqlWork.connect()
    if mysqlWork.create_table(DB_NAME, TABLES) == -1:
        mysqlWork.delete_table(DB_NAME, TB_NAME)
    mysqlWork.create_table(DB_NAME, TABLES)
    mysqlWork.close()


def test_mysql_delete():
    config = {
        'user': 'root',
        'password': '12345',
        'host': 'localhost',
    }

    DB_NAME = 'db_chess'
    TB_NAME = 'tb_chess'
    mysqlWork = MysqlWork(config)
    mysqlWork.connect()
    mysqlWork.delete_table(DB_NAME, TB_NAME)
    mysqlWork.close()


def test_mysql_insert():
    config = {
        'user': 'root',
        'password': '12345',
        'host': 'localhost',
    }
    insert_sql = ("INSERT INTO tb_chess "
                    "(count, x, y, color) "# noqa
                    "VALUES(%s, %s, %s, %s)")
    data_chess = (225, '15', '15', 2)
    DB_NAME = 'db_chess'

    mysqlWork = MysqlWork(config)
    mysqlWork.connect()
    mysqlWork.insert_data(DB_NAME, insert_sql, data_chess)
    mysqlWork.close()


def test_mysql_query():
    config = {
        'user': 'root',
        'password': '12345', 
        'host': 'localhost',
    }
    DB_NAME = 'db_chess'
    query_sql = ("SELECT * FROM tb_chess WHERE count = %s")
    data = (225,)

    mysqlWork = MysqlWork(config)
    mysqlWork.connect()
    ret = mysqlWork.query_data(DB_NAME, query_sql, data)

    for (count, x, y, color) in ret:
        print("count = {:d} x = {} y = {} color = {:d} ".format(count, x, y, color))
    mysqlWork.close()


if __name__ == '__main__':
    test_mysql_create()
