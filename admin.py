# @File: admin.py
import tkinter as tk
from tools import *
class AdminLogic:
    def __init__(self):
        pass

    def update_listbox(self, listbox, type, mode):
        listbox.delete(0, tk.END)
        keys = tools().show_data(type, "statement")["attributes"]
        lst = tools().show_data(type, mode)
        statement_str = "".join("{:<20}".format(key) for key in keys)
        listbox.insert(0, statement_str)
        for item in lst:
            row_str = "".join("{:<20}".format(item[key]) for key in keys)
            listbox.insert(tk.END, row_str)
        max_length = max(len(row_str) for row_str in listbox.get(0, tk.END))
        listbox.config(width=max_length)

    def get_object(self, listbox):
        return str(listbox.get(listbox.curselection())).split()

    def delete_accounts(self, mode, id):
        try:
            tools().delete_accounts(mode, id)
            messagebox.showinfo("删除成功", "删除成功")
        except:
            messagebox.showerror("删除失败", "删除失败")
        id.set("待操作对象ID")

