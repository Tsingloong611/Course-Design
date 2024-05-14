import tkinter as tk
from gui.main_window import MainWindow


def start():
    root = tk.Tk()
    main_window = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    start()