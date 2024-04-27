# @File: tools.py
import json
from tkinter import messagebox
import os
import shutil


class tools:
    def __init__(self):
        pass

    def load_config(self):
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                return json.load(f)
        else:
            with open("config.json", "w") as f:
                configs = {
                    "auto_backup": True
                }
                json.dump(configs, f, indent=4)
                return configs

    def save_config(self, key, value):
        config = self.load_config()
        try:
            config[key] = value
            messagebox.showinfo("成功", f"配置项{config[key]}已修改为{value}")
        except:
            messagebox.showerror("错误", "配置项不存在")

    def auto_backup(self):
        config = self.load_config()
        if config["auto_backup"] == True:
            self.backup()
            messagebox.showinfo("自动备份", "自动备份以开启，已备份数据")
        else:
            choose = messagebox.askyesno("高危操作", "自动备份已关闭，请确认是否需要备份数据")
            if choose == True:
                self.backup()
                messagebox.showinfo("手动备份", "已备份数据")

    def backup(self):
        if not os.path.exists("data_backup"):
            os.makedirs("data_backup")

        for root, _, files in os.walk("data"):
            for file in files:
                source_file = os.path.join(root, file)
                backup_file = os.path.join("data_backup", file)
                shutil.copy2(source_file, backup_file)

    def show_data(self, type, mode="all"):
        path = f"./data/{type}.json"
        with open(path, "r") as f:
            return json.load(f)[mode]

    def get_accounts(self, mode):
        with open("./data/accounts_data.json", "r") as f:
            if mode != "all":
                return json.load(f)[mode]
            else:
                return json.load(f)

    def add_accounts(self, mode, username, password):
        self.auto_backup()
        datas = self.get_accounts(mode)
        datas.append({"username": username, "password": password})
        accounts = self.get_accounts("all")
        accounts[mode] = datas
        with open("./data/accounts_data.json", "w") as f:
            json.dump(accounts, f, indent=4)
        return True

    def delete_accounts(self, mode, id):
        self.auto_backup()
        datas = self.get_accounts(mode)
        for data in datas:
            if data["id"] == id:
                datas.remove(data)
                accounts = self.get_accounts("all")
                accounts[mode] = datas
                with open("./data/accounts_data.json", "w") as f:
                    json.dump(accounts, f, indent=4)
                return True
        return False
