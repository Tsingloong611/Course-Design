# @File: main_window.py
import tkinter as tk
from tkinter import messagebox
from gui.login_window import LoginWindow
from dao.tools import tools


class MainWindow:
    def __init__(self, root):
        self.window = root
        self.window.title("学习管理系统")
        self.window.geometry("400x200")
        self.window.resizable(0, 0)
        login_button = tk.Button(self.window, text="进入认证界面", command=self.auth)
        login_button.pack()
        initialize_button = tk.Button(self.window, text="产品激活/恢复出厂模式",
                                      command=lambda: self.initialize())
        initialize_button.pack()

    def auth(self):
        if tools().check_file(r"./data/data.json", mode="check"):
            LoginWindow(tk.Toplevel(self.window))
        else:
            messagebox.showerror("错误", "数据文件不存在，请先进行激活/恢复出厂模式")
            self.initialize()

    def initialize(self):
        window = tk.Tk()
        window.title("产品激活/恢复出厂模式")
        window.geometry("400x100")
        window.resizable(0, 0)

        code_label = tk.Label(window, text="请输入激活码")
        code_label.pack()
        code_entry = tk.Entry(window)
        code_entry.pack()
        confirm_button = tk.Button(window, text="确认", command=lambda: self.confirm(code_entry.get()))
        confirm_button.pack()

    def confirm(self, code):
        if code == "123456":
            ask = tk.messagebox.askyesno("确认", "确认激活/恢复出厂模式,这将覆盖所有数据")
            if ask:
                tools().initialize()
                tk.messagebox.showinfo("成功", "操作成功")
            else:
                tk.messagebox.showinfo("取消", "操作已取消")
        else:
            tk.messagebox.showerror("错误", "激活码错误,拒绝操作")


if __name__ == "__main__":
    root = tk.Tk()
    main_window = MainWindow(root)
    root.mainloop()
