import tkinter
from tkinter import messagebox
import math
from tkinter import ttk
import socket
import threading
from ttkthemes import ThemedTk
import sys
sys.path.append('..')


from common.circle import Circle# noqa
import common.point as Point# noqa
import common.record as Record# noqa
from common.create import MysqlWork# noqa
from common.sql import Sql # noqa
from common.mainchess import MainChess# noqa


class Chess_Canvas(MainChess):
    """docstring for ClassName"""
    def __init__(self, master, height, width, HOST, PORT):
        super().__init__(master, height, width, HOST, PORT)
        self.my_color = 'white'
        self.you_color = 'black'


class Chess():
    def __init__(self, root, HOST, PORT):
        self.master = ThemedTk(theme="radiance")
        self.master.title('SERVER')
        root.destroy()
        self.create_widgets(HOST, PORT)
        self.master.mainloop()

    def create_widgets(self, HOST, PORT):
        self.chess_canvas = Chess_Canvas(self.master, 650, 630, HOST, PORT)# noqaE501

        self.chess_canvas.bind('<Button-1>', self.chess_canvas.click1)

        self.chess_canvas.pack()
        btn_reset = ttk.Button(self.master, text='REGRET', command= lambda: self.chess_canvas.regret())# noqaE501
        btn_reset.place(x=20, y=620)

        btn_quit = ttk.Button(self.master, text='QUIT', command=lambda: self.chess_canvas.quit())# noqaE501
        btn_quit.place(x=150, y=620)

        btn_play_back = ttk.Button(self.master, text='PLAY BACK', command=lambda: self.chess_canvas.play_back())# noqaE501
        btn_play_back.place(x=280, y=620)
