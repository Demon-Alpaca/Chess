import tkinter
import socket
import threading
from tkinter import messagebox
import math

from common.circle import Circle# noqa
import common.point as Point# noqa
import common.record as Record# noqa
from common.create import MysqlWork# noqa
from common.sql import Sql # noqa


class MainChess(tkinter.Canvas):
    """docstring for MainChess"""
    def __init__(self, master, height, width, HOST, PORT):
        tkinter.Canvas.__init__(self, master, height=height, width=width)
        # 回放前将数据一次读出
        self.not_prepared = True
        # 是否要新建数据库
        self.is_create_db = True
        # tb_chess 的主键
        self.count = 0
        self.is_running = True
        self.master = master
        # 用于悔棋的栈
        self.my_points = []
        self.you_points = []
        # 保存回放棋子的栈
        self.back_point = []
        # 保存数据库查询结果的队列
        self.sql_ret = []
        # 拥有的可下棋数量 User中重写
        self.canplay = 0
        self.Record = Record.Record()
        self.init_chess_board()

        # 在子类中重写
        self.my_color = ''
        self.you_color = ''
        self.HOST = str(HOST)
        self.PORT = int(PORT)
        self.init_server()

        # 数据库操作
        self.init_sql()

    def init_chess_board(self):
        self.chess_board_points = [[None for i in range(15)] for j in range(15)]# noqaE501
        for i in range(15):
            for j in range(15):
                self.chess_board_points[i][j] = Point.Point(i, j)  # noqaE501 棋盘坐标向像素坐标转化
        # 横线
        for i in range(15):
            self.create_line(self.chess_board_points[i][0].pixel_x, self.chess_board_points[i][0].pixel_y, self.chess_board_points[i][14].pixel_x, self.chess_board_points[i][14].pixel_y, fill='blue')# noqaE501
        # 竖线
        for j in range(15):
            self.create_line(self.chess_board_points[0][j].pixel_x, self.chess_board_points[0][j].pixel_y, self.chess_board_points[14][j].pixel_x, self.chess_board_points[14][j].pixel_y, fill='blue')# noqaE501
        # 线与线的交点
        for i in range(15):
            for j in range(15):
                r = 1
                self.create_oval(self.chess_board_points[i][j].pixel_x-r, self.chess_board_points[i][j].pixel_y-r, self.chess_board_points[i][j].pixel_x+r, self.chess_board_points[i][j].pixel_y+r)# noqaE501

    def init_server(self):
        ''' User需要自己在子类总重写 '''
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.HOST, self.PORT))
        self.server.listen(10)
        self.thread_1 = threading.Thread(target=self.accept_message, args=(self.server, self))# noqaE501
        self.thread_1.start()

    def init_sql(self):
        ''' User 重写此方法 '''
        # 数据库操作
        self.DB_NAME = 'db_chess'
        self.TB_NAME = 'tb_chess'
        self.config = {
            'user': 'root',
            'password': '12345',
            'host': 'localhost',
        }
        self.mysqlWork = MysqlWork(self.config)
        self.mysqlWork.connect()

        self.TABLES = {}
        # action == '1' 代表下棋 action == '0' 代表悔棋
        self.TABLES['tb_chess'] = (
            "CREATE TABLE `tb_chess`("
            "`count` int(3),"
            "`x` int(2),"
            "`y` int(2),"
            "`color` varchar(6),"
            "`action` int(1),"
            "PRIMARY KEY (`count`)"
            ") ENGINE=InnoDB"
        )
        self.query_sql = ("SELECT * FROM tb_chess")
        self.insert_sql = ("INSERT INTO tb_chess "
                            "(count, x, y, color, action) "# noqa
                            "VALUES(%s, %s, %s, %s, %s)")

    def accept_message(self, server, theSystem):
        ''' User子类中重写 '''
        conn, address = self.server.accept()
        self.sock = conn
        while self.is_running:
            data = self.sock.recv(1024).decode()
            if not data:
                break
            if data == 'delete':
                self.regrt_after_serve()
            else:
                rec_data = data.split(' ')
                x = int(rec_data[0])
                y = int(rec_data[1])
                self.call_after_sever(x, y)

    def win(self, result):
        if result == 1:
            messagebox.shoinfo(title='WIN', message='The White Win')# noqaE501
            self.unbind('<Button-1>')
        elif result == 2:
            messagebox.showinfo(title='WIN', message='The Black Win')# noqaE501
            self.unbind('<Button-1>')

    def in_table(self, x, y):
        for i in range(15):
            for j in range(15):
                square_distance = math.pow((x - self.chess_board_points[i][j].pixel_x), 2) + math.pow((y - self.chess_board_points[i][j].pixel_y), 2)# noqaE501
                if (square_distance <= 200) and (not self.Record.has_record(i, j)):# noqaE501
                    return i, j

    def create_new_table(self):
        if self.mysqlWork.create_table(self.DB_NAME, self.TABLES) == -1:
            self.mysqlWork.delete_table(self.DB_NAME, self.TB_NAME)
            self.mysqlWork.create_table(self.DB_NAME, self.TABLES)
        self.is_create_db = False

    def call_after_sever(self, x, y):
        if self.is_create_db:
            self.create_new_table()
        # tb_chess 的主键
        self.count += 1
        self.canplay += 1
        i, j = self.in_table(x, y)
        # 距离小于14并且没有落子
        point = self.create_oval(self.chess_board_points[i][j].pixel_x-10, self.chess_board_points[i][j].pixel_y-10, self.chess_board_points[i][j].pixel_x+10, self.chess_board_points[i][j].pixel_y+10, fill=self.you_color)# noqaE501
        self.Record.insert_record(i, j, color=self.you_color)
        circle = Circle(point, i, j)
        # 记录到队列中
        self.you_points.append(circle)
        result = self.Record.check()

        # 写入数据库
        data_chess = (self.count, i, j, self.you_color, 1)
        self.mysql_insert(data_chess)
        # 判断谁赢了
        self.win(result)

    def mysql_insert(self, data_chess):
        self.mysqlWork.insert_data(self.DB_NAME, self.insert_sql, data_chess)# noqaE501

    def click1(self, event):
        # tb_chess 的主键
        self.count += 1
        if self.canplay > 0:
            data = str(event.x)+" "+str(event.y)
            self.sock.send(data.encode("utf-8"))
            i, j = self.in_table(event.x, event.y)
            point = self.create_oval(self.chess_board_points[i][j].pixel_x-10, self.chess_board_points[i][j].pixel_y-10, self.chess_board_points[i][j].pixel_x+10, self.chess_board_points[i][j].pixel_y+10, fill=self.my_color)# noqaE501
            # 插入记录 用于之后判断
            self.Record.insert_record(i, j, color=self.my_color)
            # 添加进my_point队列 用于悔棋
            circle = Circle(point, i, j)
            self.my_points.append(circle)
            result = self.Record.check()
            # 写入数据库
            data_chess = (self.count, i, j, self.my_color, 1)
            self.mysql_insert(data_chess)
            # 判断是否有五子连珠
            self.win(result)
            # print("after click canplay = {:d}".format(self.canplay))

    def regret(self):
        # tb_chess 的主键
        self.count += 1
        if len(self.my_points) > 0:
            point = self.my_points.pop()
            self.delete(point.circle)
            self.Record.delete_record(point.x, point.y)
            data = 'delete'
            self.sock.send(data.encode("utf-8"))
            # 每悔棋一次 加一次下棋机会
            self.canplay += 1

            # 写入数据库
            data_chess = (self.count, point.x, point.y, self.my_color, 0)

            self.mysqlWork.insert_data(self.DB_NAME, self.insert_sql, data_chess)# noqaE501

    def regrt_after_serve(self):
        # tb_chess 的主键
        self.count += 1
        if len(self.you_points) > 0:
            point = self.you_points.pop()
            self.delete(point.circle)
            self.Record.delete_record(point.x, point.y)
            # 写入数据库
            data_chess = (self.count, point.x, point.y, self.you_color, 0)
            self.mysqlWork.insert_data(self.DB_NAME, self.insert_sql, data_chess)# noqaE501

    def quit(self):
        self.is_running = False
        self.thread_1.join()
        self.mysqlWork.close()

    # 回放前的准备工作
    def before_play_back(self):
        ''' User 重写此方法 '''
        # 将数据库查询结果存储到队列中
        self.not_prepared = False
        ret = self.mysqlWork.query_data(self.DB_NAME, self.query_sql)

        for (count, x, y, color, action) in ret:
            # print("count = {:d} x = {:d} y = {:d} color = {} action = {:d}".format(count, x, y, color, action))# noqaE501
            sql = Sql(count, x, y, color, action)
            self.sql_ret.append(sql)

    def play_back(self):
        ''' User 重写此类 '''
        if self.not_prepared:
            self.before_play_back()

        if len(self.sql_ret) > 0:
            sql = self.sql_ret.pop(0)
            x = sql.x
            y = sql.y
            color = sql.color
            action = sql.action
            if action == 1:
                point = self.create_oval(self.chess_board_points[x][y].pixel_x-10, self.chess_board_points[x][y].pixel_y-10, self.chess_board_points[x][y].pixel_x+10, self.chess_board_points[x][y].pixel_y+10, fill=color) # noqaE501
                # 插入记录 用于之后判断
                self.Record.insert_record(x, y, color=color)

                # 添加进my_point队列 用于悔棋
                circle = Circle(point, x, y)
                self.back_point.append(circle)
                result = self.Record.check()
                self.win(result)
                # time.sleep(3)
            else:
                point = self.back_point.pop()
                self.delete(point.circle)
                self.Record.delete_record(point.x, point.y)