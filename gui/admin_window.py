# @File: admin_window.py
import tkinter as tk
from tkinter import messagebox
from tools import *
from admin import AdminLogic


class AdminWindow:
    def __init__(self, root):
        self.admin_logic = AdminLogic()
        self.window = root
        self.window.title("管理员界面")
        self.window.geometry("400x400")
        self.window.resizable(0, 0)
        # 创建按钮
        self.operate_accounts_button = tk.Button(self.window, text="管理账户", command=self.operate_accounts)
        self.operate_accounts_button.pack()

        self.operate_config_button = tk.Button(self.window, text="管理配置文件", command=self.operate_config)
        self.operate_config_button.pack()




    def operate_accounts(self):
        page = tk.Toplevel(self.window)
        page.title("管理账户")
        page.geometry("600x600")

        listbox = tk.Listbox(page)
        listbox.grid(row=0, column=0, padx=10, pady=10)

        mode = tk.StringVar()
        mode.set("选择操作对象类型")

        mode_select = tk.OptionMenu(page, mode, "students", "teachers", "admins",
                                    command=lambda x: self.admin_logic.update_listbox(listbox, "accounts_data", mode.get()))
        mode_select.grid(row=1, column=1, padx=10, pady=10)

        choose_label = tk.Label(page, text="请选择操作对象类型")
        choose_label.grid(row=1, column=0, padx=10, pady=10)

        confirm_id = tk.StringVar()
        confirm_id.set("待操作对象ID")

        confirm_button = tk.Button(page, text="确认操作对象",
                                   command=lambda: confirm_id.set(self.admin_logic.get_object(listbox)[0]))
        confirm_button.grid(row=2, column=1, padx=10, pady=10)

        confirm_entry = tk.Entry(page, textvariable=confirm_id)
        confirm_entry.grid(row=2, column=0, padx=10, pady=10)

        delete_button = tk.Button(page, text="删除", command=lambda: self.admin_logic.delete_accounts(mode.get(), confirm_id.get()))
        delete_button.grid(row=3, column=0, padx=10, pady=10)

    def operate_config(self):
        page = tk.Toplevel(self.window)
        page.title("管理配置文件")
        page.geometry("300x300")
        label = tk.Label(page, text="这是页面2")
        label.pack()


if __name__ == "__main__":
    root = tk.Tk()
    admin_window = AdminWindow(root)
    root.mainloop()
