import tkinter as tk
from tkinter import messagebox, simpledialog
from gui.login_window import LoginWindow
from dao.tools import tools

class MainWindow:
    def __init__(self, root):
        """
        主界面
        :param root: 窗口
        """
        self.window = root
        self.window.title("学习管理系统")
        self.window.geometry("400x200")
        self.window.resizable(0, 0)
        self.window.configure(bg="#f0f0f0")

        login_button = tk.Button(self.window, text="进入认证界面", command=self.auth, bg="#3498db", fg="white", font=("Roboto", 12), relief=tk.RAISED)
        login_button.pack(pady=20, padx=10, ipadx=10, ipady=5)

        feedback_button = tk.Button(self.window, text="用户反馈", command=self.get_feedback, bg="#27ae60", fg="white", font=("Roboto", 12), relief=tk.RAISED)
        feedback_button.pack(pady=10, padx=10, ipadx=10, ipady=5)

    def get_feedback(self):
        """
        获取用户反馈
        :return:
        """
        feedback = simpledialog.askstring("用户反馈", "请输入您的反馈意见:", parent=self.window)
        if feedback:
            self.save_feedback(feedback)
            messagebox.showinfo("反馈提交成功", "感谢您的反馈意见！我们会认真考虑。")
        else:
            messagebox.showwarning("警告", "请输入有效的反馈意见！")

    def save_feedback(self, feedback):
        """
        保存用户反馈
        :param feedback: 反馈
        :return:
        """
        with open(r"./data/feedback.txt", "a") as file:
            file.write(feedback + "\n")

    def auth(self):
        """
        进入认证界面
        :return:
        """
        if tools().check_file(r"./data/data.json", mode="check"):
            LoginWindow(tk.Toplevel(self.window))
        else:
            messagebox.showwarning("警告", "数据文件不存在，已自动生成默认数据，管理员账户(id:0, password:123456)")
            tools().initialize()
