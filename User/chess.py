import tkinter
from tkinter import ttk
import socket
import threading
import sys
sys.path.append('..')


from common.circle import Circle# noqa
import common.point as Point# noqa
import common.record as Record# noqa
from common.mainchess import MainChess# noqa


class Chess_Canvas(MainChess):
    def __init__(self, master, height, width, HOST, PORT):
        super().__init__(master, height, width, HOST, PORT)
        self.my_color = 'black'
        self.you_color = 'white'
        self.canplay = 1

    def init_server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.HOST, self.PORT))
        print('successed')
        t1 = threading.Thread(target=self.accept_message, args=(self.sock, self))# noqaE501
        t1.start()

    def init_sql(self):
        pass

    def mysql_insert(self, data_chess):
        pass

    def create_new_table(self):
        self.is_create_db = False

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

    def before_play_back(self):
        pass

    def play_back(self):
        pass


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
