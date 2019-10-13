from ttkthemes import ThemedTk
from chess import Chess


if __name__ == '__main__':
    window = ThemedTk(theme="radiance")
    gui = Chess(window)
    window.mainloop()
