# @File: login_window.py
import tkinter as tk
from tkinter import messagebox
from logic.authentication import AuthenticationLogic
from gui.admin_window import AdminWindow
from gui.student_window import StudentWindow
from gui.teacher_window import TeacherWindow


class LoginWindow:
    def __init__(self, root):
        """
        登录界面
        :param root:
        """
        self.authentication_logic = AuthenticationLogic()
        self.window = root
        self.window.title("认证界面")
        self.window.geometry("350x250")
        self.window.resizable(0, 0)
        self.window.configure(bg="#f0f0f0")  # 设置窗口背景色为浅灰色

        # 选择登录方式
        choose_label = tk.Label(self.window, text="请选择登录方式", font=("Roboto", 12))
        choose_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.choose_radio = tk.StringVar()
        self.choose_radio.set("未指定")

        student_radio = tk.Radiobutton(self.window, text="学生", variable=self.choose_radio, value="students",
                                       font=("Roboto", 10))
        student_radio.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        teacher_radio = tk.Radiobutton(self.window, text="教师", variable=self.choose_radio, value="teachers",
                                       font=("Roboto", 10))
        teacher_radio.grid(row=1, column=1, padx=10, pady=5)

        admin_radio = tk.Radiobutton(self.window, text="管理员", variable=self.choose_radio, value="admins",
                                     font=("Roboto", 10))
        admin_radio.grid(row=1, column=2, padx=10, pady=5, sticky=tk.E)

        # 用户名和密码输入
        username_label = tk.Label(self.window, text="学(工)号:", font=("Roboto", 10))
        username_label.grid(row=2, column=0, padx=10, pady=5)

        self.id_entry = tk.Entry(self.window, font=("Roboto", 10))
        self.id_entry.grid(row=2, column=1, padx=10, pady=5)

        password_label = tk.Label(self.window, text="密码:", font=("Roboto", 10))
        password_label.grid(row=3, column=0, padx=10, pady=5)

        self.password_entry = tk.Entry(self.window, show="*", font=("Roboto", 10))
        self.password_entry.grid(row=3, column=1, padx=10, pady=5)

        # 登录按钮
        login_button = tk.Button(self.window, text="登录", command=self.login, bg="#3498db", fg="white",
                                 font=("Roboto", 12), relief=tk.RAISED)
        login_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
    def login(self):
        """
        登录
        :return:
        """
        id = self.id_entry.get()
        password = self.password_entry.get()
        mode = self.choose_radio.get()
        user = self.authentication_logic.login(id, password, mode)
        if user and mode == "students":
            messagebox.showinfo("登录成功", f"欢迎学生 {user['username']}")
            StudentWindow(tk.Toplevel(self.window), id)
        elif user and mode == "teachers":
            messagebox.showinfo("登录成功", f"欢迎教师 {user['username']}")
            TeacherWindow(tk.Toplevel(self.window), id)
        elif user and mode == "admins":
            messagebox.showinfo("登录成功", f"欢迎管理员 {user['username']}")
            AdminWindow(tk.Toplevel(self.window))
        else:
            messagebox.showerror("登录失败", "登录失败")