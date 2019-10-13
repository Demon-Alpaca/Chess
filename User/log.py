from tkinter import StringVar
from tkinter import Canvas
from tkinter import PhotoImage
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from chess import Chess
from tkinter import Tk


def log():
    root = Tk()
    root.title('17074304')
    root.geometry('600x450')

    var_HOST = StringVar()
    var_HOST.set('127.0.0.1')
    var_PORT = StringVar()
    var_PORT.set('5000')

    # 图片
    canvas = Canvas(root, height=650, width=600)
    image_file = PhotoImage(file='image/back.gif')
    canvas.create_image(0, 0, anchor='nw', image=image_file)
    canvas.pack(side='top')

    Label(root, text='HOST').place(x=50, y=50)
    Label(root, text='PORT').place(x=50, y=90)

    # 输入框
    entry_HOST = Entry(root, textvariable=var_HOST)
    entry_HOST.place(x=160, y=50)
    entry_PORT = Entry(root, textvariable=var_PORT)
    entry_PORT.place(x=160, y=90)

    # 登录注册按钮
    btn_login = Button(root, text='开始', command=lambda: Chess(root, entry_HOST.get(), entry_PORT.get()))# noqaE501
    btn_login.place(x=170, y=130)
    root.mainloop()


if __name__ == "__main__":
    log()
