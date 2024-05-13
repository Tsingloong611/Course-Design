# @File: admin.py
import tkinter as tk
from tools import *


class AdminLogic:
    def __init__(self):
        pass

    def update_account_listbox(self, listbox, type):
        listbox.delete(0, tk.END)
        keys = tools().load_data("statement")["account_attributes"]
        lst = tools().load_data(type)
        statement_str = "".join("{:<20}".format(key) for key in keys)
        listbox.insert(0, statement_str)
        configs = tools().load_config()
        show_password = configs["show_password"]
        for item in lst:
            if show_password == "0":
                row_str = "".join("{:<20}".format(item[key] if key != "password" else "******") for key in keys)
            else:
                row_str = "".join("{:<20}".format(item[key]) for key in keys)
            listbox.insert(tk.END, row_str)
        max_length = max(len(row_str) for row_str in listbox.get(0, tk.END))
        listbox.config(width=max_length)

    def update_config_listbox(self, listbox):
        listbox.delete(0, tk.END)
        keys = tools().load_data("statement")["config_attributes"]
        dict = tools().load_data(path="config.json")
        statement_str = "".join("{:<20}".format(key) for key in keys)
        listbox.insert(0, statement_str)
        for key, value in dict.items():
            row_str = "{:<20} {:<20}".format(key, value)
            listbox.insert(tk.END, row_str)
        max_length = max(len(row_str) for row_str in listbox.get(0, tk.END))
        listbox.config(width=max_length)

    def update_course_listbox(self, listbox):
        listbox.delete(0, tk.END)
        keys = tools().load_data("statement")["course_attributes"]
        lst = tools().load_data("courses")
        statement_str = "".join("{:<20}".format(key) for key in keys)
        listbox.insert(0, statement_str)
        for item in lst:
            row_str = "".join("{:<20}".format(item[key]) for key in keys)
            listbox.insert(tk.END, row_str)
        max_length = max(len(row_str) for row_str in listbox.get(0, tk.END))
        listbox.config(width=max_length)

    def get_object(self, listbox):
        return str(listbox.get(listbox.curselection())).split()

    def add_accounts(self, type, id, username, password, **kwargs):
        tools().add_accounts(type, id, username, password)
        self.reoperate(**kwargs)
        messagebox.showinfo("注册成功", f"[{type}] {id} {username} 注册成功")

    def confirm_object(self, listbox, mode, **kwargs):
        STATE = kwargs.get("state", None)
        if mode =="accounts":

            choose_object = kwargs.get("choose_object", None)

            accounts_listbox_mode = kwargs.get("accounts_listbox_mode", None)  # 列表模式
            confirm_id = kwargs.get("confirm_id", None)

            confirm_id_entry = kwargs.get("confirm_id_entry", None)
            confirm_username_entry = kwargs.get("confirm_username_entry", None)

            confirm_button = kwargs.get("confirm_button", None)
            add_button = kwargs.get("add_button", None)
            delete_button = kwargs.get("delete_button", None)
            reset_button = kwargs.get("reset_button", None)

            if accounts_listbox_mode.get() != "选择操作对象类型":
                if confirm_id.get() == "待操作对象ID":
                    if listbox.curselection():
                        if self.get_object(listbox)[0] not in ["id", "key"]:
                            confirm_id_entry.config(state=STATE[0])
                            confirm_id.set(self.get_object(listbox)[0])
                            choose_object.set(accounts_listbox_mode.get())

                            confirm_button.config(state=STATE[0])
                            delete_button.config(state=STATE[1])
                            reset_button.config(state=STATE[1])
                        else:
                            messagebox.showwarning("警告", "请正确选择列表内容作为操作对象!")
                    else:
                        messagebox.showwarning("警告", "请从列表选取对象或者手动指定对象ID")

                elif confirm_id.get() != "待操作对象ID":
                    add_button.config(state=STATE[1])
                    confirm_id_entry.config(state=STATE[0])
                    confirm_username_entry.config(state=STATE[1])
                    confirm_id.set(confirm_id.get())
                    choose_object.set(accounts_listbox_mode.get())

                    confirm_button.config(state=STATE[0])
            else:
                messagebox.showwarning("警告", "请选择操作对象类型!")

        elif mode == "configs":
            confirm_key = kwargs.get("confirm_key", None)
            if listbox.curselection():
                if self.get_object(listbox)[0] not in ["id", "key"]:
                    confirm_key.set(self.get_object(listbox)[0])
                else:
                    messagebox.showwarning("警告", "请正确选择列表内容作为操作对象!")
            else:
                messagebox.showwarning("警告", "请选择操作对象!")

        elif mode == "courses":
            confirm_id = kwargs.get("confirm_id", None)
            if listbox.curselection():
                if self.get_object(listbox)[0] not in ["id", "key"]:
                    confirm_id.set(self.get_object(listbox)[0])
                else:
                    messagebox.showwarning("警告", "请正确选择列表内容作为操作对象!")
            else:
                messagebox.showwarning("警告", "请选择操作对象!")

    def delete_accounts(self, type, id, **kwargs):
        try:
            tools().delete_accounts(type, id)
            messagebox.showinfo("删除成功", "删除成功")
        except:
            messagebox.showerror("删除失败", "删除失败")
        self.reoperate(**kwargs)

    def reset_password(self, type, id,new_password, **kwargs):
        tools().reset_password(type, id, new_password)
        self.reoperate(**kwargs)
        messagebox.showinfo("重置成功", f"[{type}] {id} 的密码重置为 {new_password}")

    def reoperate(self, **kwargs):
        STATE = kwargs.get("state", None)
        listbox = kwargs.get("listbox", None)

        choose_object = kwargs.get("choose_object", None)
        accounts_listbox_mode = kwargs.get("accounts_listbox_mode", None)  # 列表模式
        confirm_id = kwargs.get("confirm_id", None)
        confirm_password = kwargs.get("confirm_password", None)
        confirm_username = kwargs.get("confirm_username", None)
        confirm_id_entry = kwargs.get("confirm_id_entry", None)
        confirm_username_entry = kwargs.get("confirm_username_entry", None)
        confirm_button = kwargs.get("confirm_button", None)
        add_button = kwargs.get("add_button", None)
        delete_button = kwargs.get("delete_button", None)
        reset_button = kwargs.get("reset_button", None)

        accounts_listbox_mode.set("选择操作对象类型")
        choose_object.set("选择操作对象类型")
        listbox.delete(0, tk.END)
        confirm_id.set("待操作对象ID")
        confirm_password.set("新密码")
        confirm_username.set("用户名")
        confirm_username_entry.config(state=STATE[0])
        add_button.config(state=STATE[0])
        confirm_button.config(state=STATE[1])
        confirm_id_entry.config(state=STATE[1])
        delete_button.config(state=STATE[0])
        reset_button.config(state=STATE[0])

    def register_course(self, course):
        name = course["name"]
        datas = tools().load_data("courses")
        datas.append(course)
        tools().save_data(datas, "courses")
        messagebox.showinfo("注册成功", f"课程{name}注册成功")

    def confirm_register_course(self, checkboxes, id, name, term, teacher_id):
        if id == "" or name == "" or term == "" or teacher_id == "":
            messagebox.showerror("错误", "请填写完整信息")
            return
        elif not id.isdigit() or not teacher_id.isdigit():
            messagebox.showerror("错误", "课程/教师id必须为数字")
            return
        elif id in [course["id"] for course in tools().load_data(type="courses")]:
            messagebox.showerror("错误", "课程id已存在")
            return
        elif teacher_id not in [teacher["id"] for teacher in tools().load_data(type="teachers")]:
            messagebox.showerror("错误", "教师id不存在")
            return
        else:
            course_data = {
                "id": id,
                "name": name,
                "term": term,
                "time": [],
                "teacher_id": teacher_id,
                "student_ids": []
            }

            for key, var in checkboxes.items():
                if var.get() == 1:
                    week, day, time = key.split()
                    time_added = False
                    for item in course_data["time"]:
                        if item["week"] == week and item["day"] == day:
                            item["time"].append(time)
                            time_added = True
                            break

                    if not time_added:
                        course_data["time"].append({
                            "week": week,
                            "day": day,
                            "time": [time]
                        })
            self.register_course(course_data)

    def delete_courses(self, id):
        tools().delete_accounts(type="courses", id=id)
