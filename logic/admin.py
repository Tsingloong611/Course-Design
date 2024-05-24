# @File: admin.py
import tkinter as tk
from tkinter import messagebox
from dao.tools import *


class AdminLogic:
    def __init__(self):
        pass

    def update_account_listbox(self, listbox, type):
        """
        更新账户列表
        :param listbox: 列表对象
        :param type: 账户类型
        :return:
        """
        listbox.delete(0, tk.END)
        keys = tools().load_data("statements")["account_attributes"]
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
        """
        更新配置列表
        :param listbox: 列表对象
        :return:
        """
        listbox.delete(0, tk.END)
        keys = tools().load_data("statements")["config_attributes"]
        dict = tools().load_data(path="config.json")
        statement_str = "".join("{:<20}".format(key) for key in keys)
        listbox.insert(0, statement_str)
        for key, value in dict.items():
            row_str = "{:<20} {:<20}".format(key, value)
            listbox.insert(tk.END, row_str)
        max_length = max(len(row_str) for row_str in listbox.get(0, tk.END))
        listbox.config(width=max_length)

    def update_course_listbox(self, listbox):
        """
        更新课程列表
        :param listbox: 列表对象
        :return:
        """
        listbox.delete(0, tk.END)
        keys = tools().load_data("statements")["course_attributes"]
        lst = tools().load_data("courses")
        statement_str = "".join("{:<20}".format(key) for key in keys)
        listbox.insert(0, statement_str)
        for item in lst:
            row_str = "".join("{:<20}".format(item[key]) for key in keys)
            listbox.insert(tk.END, row_str)
        max_length = max(len(row_str) for row_str in listbox.get(0, tk.END))
        listbox.config(width=max_length)

    def get_object(self, listbox):
        """
        获取列表框选中的对象的以空格分隔的字符串的列表
        :param listbox:
        :return: 以空格分隔的字符串的列表
        """
        return str(listbox.get(listbox.curselection())).split()

    def add_accounts(self, type, id, username, password, **kwargs):
        """
        添加账户
        :param type: 账户类型
        :param id: id
        :param username: 用户名
        :param password: 密码
        :param kwargs: 早期设计的参数，现在已经不再使用，但是为了兼容性保留
        :return:
        """
        tools().operate_accounts(mode="add", type=type, id=id, username=username, password=password)
        self.reoperate(**kwargs)

    def confirm_object(self, listbox, mode, **kwargs):
        """
        确认操作对象
        :param listbox: 列表框对象
        :param mode: 模式
        :param kwargs: 可选参数(待续)
        :return:
        """
        STATE = kwargs.get("state", None)
        if mode == "accounts":

            choose_object = kwargs.get("choose_object", None)

            accounts_listbox_mode = kwargs.get("accounts_listbox_mode", None)  # 列表模式
            confirm_id = kwargs.get("confirm_id", None)

            confirm_id_entry = kwargs.get("confirm_id_entry", None)
            confirm_username_entry = kwargs.get("confirm_username_entry", None)

            confirm_button = kwargs.get("confirm_button", None)
            add_button = kwargs.get("add_button", None)
            delete_button = kwargs.get("delete_button", None)
            reset_button = kwargs.get("reset_button", None)
            button_normal_style = kwargs.get("button_normal_style", None)
            button_disabled_style = kwargs.get("button_disabled_style", None)

            if accounts_listbox_mode.get() != "选择操作对象类型":
                if confirm_id.get() == "待操作对象ID":
                    if listbox.curselection():
                        if self.get_object(listbox)[0] not in ["id", "key"]:
                            confirm_id_entry.config(state=STATE[0], **button_disabled_style)
                            confirm_id.set(self.get_object(listbox)[0])
                            choose_object.set(accounts_listbox_mode.get())

                            confirm_button.config(state=STATE[0], **button_disabled_style)
                            delete_button.config(state=STATE[1], **button_normal_style)
                            reset_button.config(state=STATE[1], **button_normal_style)
                        else:
                            messagebox.showwarning("警告", "请正确选择列表内容作为操作对象!")
                    else:
                        messagebox.showwarning("警告", "请从列表选取对象或者手动指定对象ID")

                elif confirm_id.get() != "待操作对象ID":
                    add_button.config(state=STATE[1], **button_normal_style)
                    confirm_id_entry.config(state=STATE[0])
                    confirm_username_entry.config(state=STATE[1])
                    confirm_id.set(confirm_id.get())
                    choose_object.set(accounts_listbox_mode.get())

                    confirm_button.config(state=STATE[0], **button_disabled_style)
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
        """
        删除账户
        :param type: 类型
        :param id: 用户id
        :param kwargs: 组件参数
        :return:
        """
        try:
            tools().operate_accounts(mode="delete", type=type, id=id)
            if type == "teachers":
                datas = tools().load_data("courses")
                for data in datas:
                    if data["teacher_id"] == id:
                        self.delete_courses(data["id"])
                        messagebox.showinfo("删除成功", f"成功删除教师 {id} 的课程 {data['id']}")
            messagebox.showinfo("删除成功", f"删除{type} {id} 成功")
        except:
            messagebox.showerror("删除失败", "删除失败")
        self.reoperate(**kwargs)

    def reset_password(self, type, id, new_password, **kwargs):
        """
        重置密码
        :param type: 类型
        :param id: 用户id
        :param new_password: 新密码
        :param kwargs: 组件参数
        :return:
        """
        tools().operate_accounts(mode="reset", type=type, id=id, new_password=new_password)
        self.reoperate(**kwargs)
        messagebox.showinfo("重置成功", f"[{type}] {id} 的密码重置为 {new_password}")

    def reoperate(self, **kwargs):
        """
        重新操作
        :param kwargs: 复原组件参数
        :return:
        """
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
        button_normal_style = kwargs.get("button_normal_style")
        button_disabled_style = kwargs.get("button_disabled_style")

        accounts_listbox_mode.set("选择操作对象类型")
        choose_object.set("选择操作对象类型")
        listbox.delete(0, tk.END)
        confirm_id.set("待操作对象ID")
        confirm_password.set("新密码")
        confirm_username.set("用户名")
        confirm_username_entry.config(state=STATE[0])
        add_button.config(state=STATE[0], **button_disabled_style)
        confirm_button.config(state=STATE[1], **button_normal_style)
        confirm_id_entry.config(state=STATE[1])
        delete_button.config(state=STATE[0], **button_disabled_style)
        reset_button.config(state=STATE[0], **button_disabled_style)

    def register_course(self, course):
        """
        注册课程
        :param course: 课程的相关信息
        :return:
        """
        name = course["name"]
        teacher_id = course["teacher_id"]
        id = course["id"]
        new_term = course["term"]

        # 在教师数据中添加教师的教授课程
        teachers = tools().load_data("teachers")
        teacher = tools().load_data("teachers", teacher_id)
        teacher["teaching_courses"].append({"course_id": id})
        for i in range(len(teachers)):
            if teachers[i]["id"] == teacher_id:
                teachers[i] = teacher
                break
        tools().save_data(type="teachers", new_datas=teachers)

        # 在课程数据中添加课程
        course_datas = tools().load_data("courses")
        course_datas.append(course)
        tools().save_data(course_datas, "courses")

        # 在学期数据中添加学期
        statements_datas = tools().load_data("statements")
        if new_term not in statements_datas["term_names"]:
            statements_datas["term_names"].append(new_term)
        tools().save_data(statements_datas, "statements")

        messagebox.showinfo("注册成功", f"课程{name}注册成功")

    def confirm_register_course(self, checkboxes, id, name, term,room, teacher_id):
        """
        确认注册课程，检查课程信息是否完整
        :param checkboxes: 时间信息
        :param id: 课程id
        :param name: 课程名
        :param term: 课程学期
        :param teacher_id: 授课教师id
        :return:
        """
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
                "room": room,
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
        """
        删除课程
        :param id: 课程id
        :return:
        """
        # 判断是否删除对应学期
        term = tools().load_data("courses", id)["term"]
        a = 0
        for course in tools().load_data("courses"):
            if course["term"] == term:
                a = 1
                break
        if a == 0:
            statements_datas = tools().load_data("statements")
            statements_datas["term_names"].remove(term)
            tools().save_data(statements_datas, "statements")
        # 删除课程
        tools().operate_accounts(mode="delete", type="courses", id=id)
        # 删除教师数据中的教授课程
        datas = tools().load_data("teachers")
        for data in datas:
            courses = data["teaching_courses"]
            for course in courses:
                if course["course_id"] == id:
                    courses.remove(course)
                    break
        tools().save_data(datas, "teachers")
        messagebox.showinfo("删除成功", f"成功删除课程 {id}")

    def change_config(self, confirm_key, confirm_value):
        """
        修改配置
        :param confirm_key: 键
        :param confirm_value: 值
        :return:
        """
        return tools().save_config(confirm_key, confirm_value)

    def get_week_num(self):
        """
        获取周数
        :return: int类型的周数
        """
        return int(tools().load_config()["week_num"])


    def confirm_init(self, code):
        """
        确认初始化数据
        :param code: 确认码
        :return:
        """
        if code == "123456":
            ask = tk.messagebox.askyesno("确认", "确认初始化数据,这将覆盖所有数据")
            if ask:
                tools().initialize()
                tk.messagebox.showinfo("成功", "操作成功")
            else:
                tk.messagebox.showinfo("取消", "操作已取消")
        else:
            tk.messagebox.showerror("错误", "确认码错误,拒绝操作")
