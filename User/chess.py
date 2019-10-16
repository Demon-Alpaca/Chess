import tkinter
from tkinter import messagebox
import math
from tkinter import ttk
import socket
import threading
import sys
sys.path.append('..')


from common.circle import Circle# noqa
import common.point as Point# noqa
import common.record as Record# noqa


class Chess_Canvas(tkinter.Canvas):
    def __init__(self, master, height, width, HOST, PORT):
        tkinter.Canvas.__init__(self, master, height=height, width=width)
        self.master = master
        self.is_running = True
        self.my_points = []
        self.you_points = []
        self.canplay = 1
        self.Record = Record.Record()
        self.chess_board_points = [[None for i in range(15)] for j in range(15)]# noqaE501
        for i in range(15):
            for j in range(15):
                self.chess_board_points[i][j] = Point.Point(i, j)  # noqaE501 棋盘坐标向像素坐标转化
        # 横线
        for i in range(15):
            self.create_line(self.chess_board_points[i][0].pixel_x, self.chess_board_points[i][0].pixel_y, self.chess_board_points[i][14].pixel_x, self.chess_board_points[i][14].pixel_y, fill='pink')# noqaE501
        # 竖线
        for j in range(15):
            self.create_line(self.chess_board_points[0][j].pixel_x, self.chess_board_points[0][j].pixel_y, self.chess_board_points[14][j].pixel_x, self.chess_board_points[14][j].pixel_y, fill='pink')# noqaE501
        # 线与线的交点
        for i in range(15):
            for j in range(15):
                r = 1
                self.create_oval(self.chess_board_points[i][j].pixel_x-r, self.chess_board_points[i][j].pixel_y-r, self.chess_board_points[i][j].pixel_x+r, self.chess_board_points[i][j].pixel_y+r)# noqaE501
        self.x = ''
        self.y = ''
        self.HOST = str(HOST)
        self.PORT = int(PORT)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.HOST, self.PORT))
        print('successed')
        t1 = threading.Thread(target=self.accept_message, args=(self.client, self))# noqaE501
        t1.start()

    def accept_message(self, client, theSystem):
        while self.is_running:
            data = client.recv(1024).decode()
            if not data:
                break
            if data == 'delete':
                self.regrt_after_serve()
            else:
                rec_data = data.split(' ')
                x = int(rec_data[0])
                y = int(rec_data[1])
                self.call_after_sever(x, y)

    def call_after_sever(self, x, y):
        self.canplay += 1
        for i in range(15):
            for j in range(15):
                square_distance = math.pow((x - self.chess_board_points[i][j].pixel_x), 2) + math.pow((y - self.chess_board_points[i][j].pixel_y), 2)# noqaE501

                if (square_distance <= 196) and (not self.Record.has_record(i, j)):# noqaE501
                    # 距离小于14并且没有落子
                    point = self.create_oval(self.chess_board_points[i][j].pixel_x-10, self.chess_board_points[i][j].pixel_y-10, self.chess_board_points[i][j].pixel_x+10, self.chess_board_points[i][j].pixel_y+10, fill='white')# noqaE501

                    self.Record.insert_record(i, j, color='white')

                    result = self.Record.check()
                    circle = Circle(point, i, j)
                    self.you_points.append(circle)
                    # 判断是否有五子连珠

                    if result == 1:
                        messagebox.shoinfo(title='WIN', message='The White Win')# noqaE501
                        # 解除鼠标左键绑定
                        self.unbind('<Button-1>')
                        # """Unbind for this widget for event SEQUENCE  the
                        #     function identified with FUNCID."""

                    elif result == 2:
                        messagebox.showinfo(title='WIN', message='The Black Win')# noqaE501
                        # 解除鼠标左键绑定
                        self.unbind('<Button-1>')

    def click1(self, event):
        if self.canplay > 0:
            data = str(event.x)+" "+str(event.y)
            self.client.send(data.encode("utf-8"))
            for i in range(15):
                for j in range(15):
                    square_distance = math.pow((event.x - self.chess_board_points[i][j].pixel_x), 2) + math.pow((event.y - self.chess_board_points[i][j].pixel_y), 2)# noqaE501

                    if (square_distance <= 196) and (not self.Record.has_record(i, j)):# noqaE501
                        # 距离小于14并且没有落子
                        point = self.create_oval(self.chess_board_points[i][j].pixel_x-10, self.chess_board_points[i][j].pixel_y-10, self.chess_board_points[i][j].pixel_x+10, self.chess_board_points[i][j].pixel_y+10, fill='black')# noqaE501

                        self.Record.insert_record(i, j, color='black')
                        circle = Circle(point, i, j)
                        self.my_points.append(circle)
                        result = self.Record.check()
                        # 判断是否有五子连珠

                        if result == 1:
                            messagebox.showinfo(title='WIN', message='The White Win')# noqaE501
                            # 解除鼠标左键绑定
                            self.unbind('<Button-1>')
                            # """Unbind for this widget for event SEQUENCE  the
                            #     function identified with FUNCID."""

                        elif result == 2:
                            messagebox.showinfo(title='WIN', message='The Black Win')# noqaE501
                            # 解除鼠标左键绑定
                            self.unbind('<Button-1>')
            self.canplay -= 1

    def regret(self):
        if len(self.my_points) > 0:
            point = self.my_points.pop()
            self.delete(point.circle)
            self.Record.delete_record(point.x, point.y)
            data = 'delete'
            self.client.send(data.encode("utf-8"))
            # 悔棋获得下棋机会
            self.canplay += 1

    def regrt_after_serve(self):
        if len(self.you_points) > 0:
            point = self.you_points.pop()
            self.Record.delete_record(point.x, point.y)
            self.delete(point.circle)

    def quit(self):
        self.is_running = False
        self.master.destroy()


class Chess():
    def __init__(self, root, HOST, PORT):
        self.master = tkinter.Tk()
        self.master.title('USER')
        root.destroy()
        self.create_widgets(HOST, PORT)
        self.master.mainloop()

    def create_widgets(self, HOST, PORT):
        self.chess_canvas = Chess_Canvas(self.master, 650, 630, HOST, PORT)# noqaE501

        self.chess_canvas.bind('<Button-1>', self.chess_canvas.click1)

        self.chess_canvas.pack()
        btn_reset = ttk.Button(self.master, text='RESET', command=lambda: self.chess_canvas.regret())# noqaE501
        btn_reset.place(x=20, y=620)

        # btn_quit = ttk.Button(self.master, text='QUIT', command=lambda: self.chess_canvas.quit())# noqaE501
        # btn_quit.place(x=100, y=620)
