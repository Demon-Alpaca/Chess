import tkinter
from tkinter import messagebox
import math
import Point
import Record
from tkinter import ttk
import socket
import threading


class Chess_Canvas(tkinter.Canvas):
    def __init__(self, master, height, width, HOST, PORT):
        tkinter.Canvas.__init__(self, master, height=height, width=width)
        self.canplay = False
        self.Record = Record.Record()
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
        self.x = ''
        self.y = ''
        self.HOST = str(HOST)
        self.PORT = int(PORT)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.HOST, self.PORT))
        self.server.listen(10)
        thread_1 = threading.Thread(target=self.accept_message, args=(self.server, self.x, self.y, self))# noqaE501
        thread_1.start()

    def accept_message(self, server, x, y, theSystem):
        conn, address = server.accept()
        theSystem.sock = conn
        print("Connection from " + str(address))
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            rec_data = data.split(' ')
            x = int(rec_data[0])
            y = int(rec_data[1])
            self.call_after_sever(x, y)

    def call_after_sever(self, x, y):
        for i in range(15):
            for j in range(15):
                square_distance = math.pow((x - self.chess_board_points[i][j].pixel_x), 2) + math.pow((y - self.chess_board_points[i][j].pixel_y), 2)# noqaE501

                if (square_distance <= 200) and (not self.Record.has_record(i, j)):# noqaE501
                    # 距离小于14并且没有落子
                    if self.Record.who_to_play() == 1:
                        # 若果根据步数判断是奇数次,那么白下
                        self.create_oval(self.chess_board_points[i][j].pixel_x-10, self.chess_board_points[i][j].pixel_y-10, self.chess_board_points[i][j].pixel_x+10, self.chess_board_points[i][j].pixel_y+10, fill='white')# noqaE501

                    elif self.Record.who_to_play() == 2:
                        self.create_oval(self.chess_board_points[i][j].pixel_x-10, self.chess_board_points[i][j].pixel_y-10, self.chess_board_points[i][j].pixel_x+10, self.chess_board_points[i][j].pixel_y+10, fill='black')# noqaE501

                    self.Record.insert_record(i, j)

                    result = self.Record.check()
                    # 判断是否有五子连珠

                    if result == 1:
                        messagebox.shoinfo(title='WIN', message='The White Win')# noqaE501
                        # 解除鼠标左键绑定
                        self.unbind('<Button-1>')

                    elif result == 2:
                        messagebox.showinfo(title='WIN', message='The Black Win')# noqaE501
                        # 解除鼠标左键绑定
                        self.unbind('<Button-1>')
        self.canplay = True

    def click1(self, event):
        if self.canplay:
            data = str(event.x)+" "+str(event.y)
            self.sock.send(data.encode("utf-8"))
            for i in range(15):
                for j in range(15):
                    square_distance = math.pow((event.x - self.chess_board_points[i][j].pixel_x), 2) + math.pow((event.y - self.chess_board_points[i][j].pixel_y), 2)# noqaE501

                    if (square_distance <= 200) and (not self.Record.has_record(i, j)):# noqaE501
                        # 距离小于14并且没有落子
                        if self.Record.who_to_play() == 1:
                            # 若果根据步数判断是奇数次,那么白下
                            self.create_oval(self.chess_board_points[i][j].pixel_x-10, self.chess_board_points[i][j].pixel_y-10, self.chess_board_points[i][j].pixel_x+10, self.chess_board_points[i][j].pixel_y+10, fill='white')# noqaE501

                        elif self.Record.who_to_play() == 2:
                            self.create_oval(self.chess_board_points[i][j].pixel_x-10, self.chess_board_points[i][j].pixel_y-10, self.chess_board_points[i][j].pixel_x+10, self.chess_board_points[i][j].pixel_y+10, fill='black')# noqaE501

                        self.Record.insert_record(i, j)

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
        self.canplay = False


class Chess():
    def __init__(self, root, HOST, PORT):
        self.master = tkinter.Tk()
        self.master.title('SERVER')
        root.destroy()
        self.create_widgets(HOST, PORT)
        self.master.mainloop()

    def create_widgets(self, HOST, PORT):
        self.chess_board_canvas = Chess_Canvas(self.master, 650, 630, HOST, PORT)# noqaE501

        self.chess_board_canvas.bind('<Button-1>', self.chess_board_canvas.click1)

        self.chess_board_canvas.pack()
        btn_reset = ttk.Button(self.master, text='RESET')# noqaE501
        btn_reset.place(x=20, y=620)
