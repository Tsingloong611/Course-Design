# @File: main_window.py
import tkinter as tk

from gui.login_window import LoginWindow


class MainWindow:
    def __init__(self, root):
        self.window = root
        self.window.title("学习管理系统")
        self.window.geometry("400x400")
        self.window.resizable(0, 0)
        login_button = tk.Button(self.window, text="进入认证界面", command=self.auth)
        login_button.grid(row=0, column=0, padx=10, pady=10)

    def auth(self):
        LoginWindow(tk.Toplevel(self.window))


if __name__ == "__main__":
    root = tk.Tk()
    main_window = MainWindow(root)
    root.mainloop()
