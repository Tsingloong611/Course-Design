# @File: tools.py
import json
from tkinter import messagebox
import os
import shutil


class tools:
    def __init__(self):
        pass

    def load_config(self):
        """
        加载配置文件
        :return: 返回配置文件的字典
        """
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                return json.load(f)
        else:
            with open("config.json", "w") as f:
                configs = {
                    "auto_backup": "1",
                    "allow_course_conflict": "0",
                    "show_password": "0",
                    "week_num": "10"
                }
                json.dump(configs, f, indent=4)
                return configs

    def save_config(self, key, value):
        """
        保存配置文件
        :param key: 配置项
        :param value: 值
        :return:
        """
        config = self.load_config()
        try:
            config[key] = value
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)
            messagebox.showinfo("成功", f"配置项{key}已修改为{value}")
        except:
            messagebox.showerror("错误", "配置项不存在")

    def auto_backup(self):
        """
        自动备份数据
        :return:
        """
        config = self.load_config()
        if config["auto_backup"] != "0":
            self.backup()
            messagebox.showinfo("自动备份", "自动备份以开启，已备份数据")
        else:
            choose = messagebox.askyesno("高危操作", "自动备份已关闭，请确认是否需要备份数据")
            if choose == True:
                self.backup()
                messagebox.showinfo("手动备份", "已备份数据")

    def backup(self):
        """
        备份数据
        :return:
        """
        if not os.path.exists("data_backup"):
            os.makedirs("data_backup")

        for root, _, files in os.walk("data"):
            exclude_dirs = self.load_config()["exclude_dirs"]  # 要排除的目录列表
            exclude_files = self.load_config()["exclude_files"]  # 要排除的文件列表

            for root, _, files in os.walk("data"):
                # 检查当前目录是否在排除列表中，如果在则跳过该目录
                if os.path.basename(root) in exclude_dirs:
                    continue

                for file in files:
                    if file in exclude_files:
                        continue

                    source_file = os.path.join(root, file)
                    backup_file = os.path.join("data_backup", file)
                    shutil.copy2(source_file, backup_file)

    def load_data(self, type="all", id="all", path=r"./data/data.json"):
        """
        加载数据
        :param mode: 加载数据的模式
        :param type: 要加载的数据类型
        :param id: 数据id
        :return: 返回指定id的数据的字典(如果id为"all"则返回所有数据的列表)
        """

        with open(path, "r") as f:
            datas = json.load(f)
            if type == "all":
                return datas
            else:
                datas = datas[type]
                if id == "all":
                    return datas
                else:
                    for data in datas:
                        if data["id"] == id:
                            return data

    def operate_accounts(self, mode, type, id, **kwargs):
        """
        操作账户
        :param mode: 操作类型
        :param type: 数据类型
        :param id: 数据id
        :param **kwargs: 其他可能参数
        :return: 对应的操作结果
        """
        self.auto_backup()
        if mode == "delete":
            return self.delete_accounts(type, id)
        elif mode == "reset":
            new_password = kwargs["new_password"]
            return self.reset_password(type, id, new_password)
        elif mode == "load":
            return self.load_data(type, id)
        elif mode == "add":
            username = kwargs["username"]
            password = kwargs["password"]
            return self.add_accounts(type, id, username, password)

    def delete_accounts(self, type, id):
        """
        删除数据
        :param type: 数据类型
        :param id: 数据id
        :return:
        """
        datas = self.load_data(type)
        new_datas = [data for data in datas if data["id"] != id]
        self.save_data(new_datas, type)

    def add_accounts(self, type, id, username, password):
        """
        添加数据
        :param type: 数据类型
        :param id: 数据id
        :param username: 用户名
        :param password: 密码
        :return:
        """
        students = {"id": id, "username": username, "password": password,
                    "enrolled_courses": [{"course_id": "0", "grade": "100"}]}

        teachers = {"id": id, "username": username, "password": password, "teaching_courses": [{"course_id": "0"}]}

        admins = {"id": id, "username": username, "password": password}
        datas = self.load_data(type=type)
        i = 1
        for data in datas:
            if data["id"] == id:
                messagebox.showerror("错误", "该id已存在")
                i = 0
                break
        if i == 1:
            if type == "students":
                datas.append(students)
            elif type == "teachers":
                datas.append(teachers)
            elif type == "admins":
                datas.append(admins)
            messagebox.showinfo("注册成功", f"[{type}] {id} {username} 注册成功")
            self.save_data(datas, type)

    def reset_password(self, type, id, new_password):
        """
        重置密码
        :param type: 数据类型
        :param id: 数据id
        :param new_password: 密码
        :return:
        """
        datas = self.load_data(type=type)
        for data in datas:
            if data["id"] == id:
                data["password"] = new_password
                self.save_data(datas, type)

    def save_data(self, new_datas, type):
        """
        保存数据
        :param type: 数据类型
        :param new_datas: 数据(列表)
        :return:
        """
        datas = self.load_data()
        datas[type] = new_datas
        with open("./data/data.json", "w") as f:
            json.dump(datas, f, indent=4)

    def check_file(self, path):
        """
        检查文件是否存在，不存在则创建
        :param path: 文件路径
        :return:
        """
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as file:
                json.dump([], file)

    def check_dir(self, path):
        """
        检查目录是否存在，不存在则创建
        :param path: 目录路径
        :return:
        """
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)

    def get_info(self, type, id, mode="username"):
        """
        获取数据信息
        :param type: 数据类型
        :param id: 数据id
        :param mode: 数据键
        :return: 返回数据键对应的值(字符串或者列表)
        """
        obj = self.load_data(type=type, id=id)
        return obj[mode]

    def initialize(self):
        statement = {
            "account_attributes": ["id", "username", "password"],
            "config_attributes": ["key", "value"],
            "course_attributes": ["id", "name", "term", "teacher_id"],
        }
        students = [
            {"id": "1", "username": "student_test", "password": "1",
             "enrolled_courses": [{"course_id": "0", "grade": "100"}]},
        ]

        teachers = [
            {"id": "1", "username": "teacher_test", "password": "1", "teaching_courses": [{"course_id": "0"}]}
        ]

        admins = [
            {"id": "1", "username": "admin_test", "password": "1"}
        ]

        courses = [{
            "id": "1",
            "name": "test_course",
            "term": "1",
            "time": [],
            "teacher_id": "1",
            "student_ids": []
        }]

        accounts = {"statement": statement, "students": students, "teachers": teachers, "admins": admins,
                    "courses": courses}

        configs = {
            "auto_backup": "1",
            "allow_course_conflict": "0",
            "show_password": "0",
            "week_num": "10",
            "exclude_dirs": ["materials_data"],
            "exclude_files": []
        }

        with open("./data/data.json", "w") as f:
            json.dump(accounts, f, indent=4)

        with open("config.json", "w") as f:
            json.dump(configs, f, indent=4)
