# @File: login_window.py
import tkinter as tk
from tkinter import messagebox
from authentication import AuthenticationLogic
from gui.admin_window import AdminWindow


class LoginWindow:
    def __init__(self, root):
        self.authentication_logic = AuthenticationLogic()
        self.window = root
        self.window.title("认证界面")
        self.window.geometry("350x200")
        self.window.resizable(0, 0)

        self.choose_label = tk.Label(self.window, text="请选择登录方式")
        self.choose_label.grid(row=0, column=0, padx=10, pady=10)

        self.choose_radio = tk.StringVar()
        self.choose_radio.set("未指定")

        self.student_radio = tk.Radiobutton(self.window, text="学生", variable=self.choose_radio, value="students")
        self.student_radio.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        self.teacher_radio = tk.Radiobutton(self.window, text="教师", variable=self.choose_radio, value="teachers")
        self.teacher_radio.grid(row=0, column=1, padx=10, pady=10, sticky=tk.E)

        self.admin_radio = tk.Radiobutton(self.window, text="管理员", variable=self.choose_radio, value="admins")
        self.admin_radio.grid(row=0, column=2, padx=10, pady=10, sticky=tk.W)

        self.username_label = tk.Label(self.window, text="学(工)号:")
        self.username_label.grid(row=1, column=0, padx=10, pady=10)

        self.id_entry = tk.Entry(self.window)
        self.id_entry.grid(row=1, column=1, padx=10, pady=10)

        self.password_label = tk.Label(self.window, text="密码:")
        self.password_label.grid(row=2, column=0, padx=10, pady=10)

        self.password_entry = tk.Entry(self.window, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)

        self.login_button = tk.Button(self.window, text="登录", command=self.login)
        self.login_button.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

    def login(self):
        id = self.id_entry.get()
        password = self.password_entry.get()
        mode = self.choose_radio.get()
        user = self.authentication_logic.login(id, password, mode)
        if user and mode == "students":
            messagebox.showinfo("登录成功", f"欢迎学生{user['username']}")
        elif user and mode == "teachers":
            messagebox.showinfo("登录成功", f"欢迎教师{user['username']}")
        elif user and mode == "admins":
            messagebox.showinfo("登录成功", f"欢迎管理员{user['username']}")
            AdminWindow(tk.Toplevel(self.window))
        else:
            messagebox.showerror("登录失败", "登录失败")


if __name__ == "__main__":
    root = tk.Tk()
    login_window = LoginWindow(root)
    root.mainloop()
