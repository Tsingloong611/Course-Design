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
        for item in lst:
            row_str = "".join("{:<20}".format(item[key] if key != "password" else "******") for key in keys)
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

    def add_accounts(self, type, id, username, password):
        print(type, id, username, password)
        tools().add_accounts(type, id, username, password)

    def confirm_object(self, listbox, **kwargs):
        confirm_id = kwargs.get("confirm_id", None)
        confirm_button = kwargs.get("confirm_button", None)
        button_mode = kwargs.get("button_mode", None)
        confirm_entry = kwargs.get("confirm_entry", None)
        delete_button = kwargs.get("delete_button", None)
        reset_button = kwargs.get("reset_button", None)
        choose_entry = kwargs.get("choose_entry", None)
        if self.get_object(listbox)[0] not in ["id", "key"]:
            confirm_id.set(self.get_object(listbox)[0])
            choose_entry.config(text=confirm_button.cget("text"))
            choose_entry.config(state=button_mode[1])
            confirm_button.config(state=button_mode[1])
            confirm_entry.config(state=button_mode[1])
            delete_button.config(state=button_mode[0])
            reset_button.config(state=button_mode[0])
        else:
            messagebox.showwarning("警告", "请正确选择操作对象!")

    def delete_accounts(self, type, confirm_id, confirm_button, confirm_entry, delete_button, reset_button,
                        button_mode):
        id = confirm_id.get()
        try:
            tools().delete_accounts(type, id)
            confirm_button.config(state=button_mode[0])
            confirm_entry.config(state=button_mode[0])
            delete_button.config(state=button_mode[1])
            reset_button.config(state=button_mode[1])
            messagebox.showinfo("删除成功", "删除成功")
        except:
            messagebox.showerror("删除失败", "删除失败")
        confirm_id.set("待操作对象ID")

    def reset_password(self, type, confirm_id, confirm_password, confirm_button, confirm_entry, delete_button,
                       reset_button,
                       button_mode):
        id = confirm_id.get()
        new_password = confirm_password.get()
        tools().reset_password(type, id, new_password)
        confirm_button.config(state=button_mode[0])
        confirm_entry.config(state=button_mode[0])
        delete_button.config(state=button_mode[1])
        reset_button.config(state=button_mode[1])
        messagebox.showinfo("重置成功", f"{type}{id}的密码重置为{new_password}")

    def reoperate(self, list_mode, listbox, confirm_id, confirm_password, confirm_button, confirm_entry, delete_button,
                  reset_button, button_mode):
        list_mode.set("选择操作对象类型")
        listbox.delete(0, tk.END)
        confirm_id.set("待操作对象ID")
        confirm_password.set("新密码")
        confirm_button.config(state=button_mode[0])
        confirm_entry.config(state=button_mode[0])
        delete_button.config(state=button_mode[1])
        reset_button.config(state=button_mode[1])

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
