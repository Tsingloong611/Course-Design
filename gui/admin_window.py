# @File: admin_window.py
import tkinter as tk
from tkinter import messagebox, ttk
from logic.admin import AdminLogic


class AdminWindow:
    def __init__(self, root):
        """
        管理员界面
        :param root: 窗口
        """
        self.admin_logic = AdminLogic()
        self.window = root
        self.window.title("管理员界面")
        self.window.geometry("300x300")
        self.window.resizable(0, 0)
        self.window.configure(bg="#f0f0f0")

        buttons = [
            ("管理账户", self.operate_accounts),
            ("管理配置文件", self.operate_config),
            ("开通课程", self.register_courses),
            ("删除课程", self.delete_courses),
            ("初始化数据", self.initialize_page)
        ]

        for text, command in buttons:
            button = tk.Button(self.window, text=text, command=command, bg="#3498db", fg="white", font=("Roboto", 12),
                               relief=tk.RAISED)
            button.pack(pady=10, padx=10, ipadx=10, ipady=5)

    def operate_accounts(self):
        """
        管理账户界面
        :return:
        """
        page = tk.Toplevel(self.window)
        page.title("管理账户")
        page.geometry("1000x600")

        # 常变量区
        button_normal_style = {"font": ("Arial", 12), "bg": "#3498db", "fg": "white", "relief": tk.RAISED}
        button_disabled_style = {"font": ("Arial", 12), "bg": "#bdc3c7", "fg": "#7f8c8d", "relief": tk.FLAT}
        STATE = ("disabled", "normal")

        # 账户可视化区
        accounts_listbox = tk.Listbox(page)
        accounts_listbox.grid(row=0, column=0, padx=10, pady=10)

        accounts_listbox_mode = tk.StringVar()
        accounts_listbox_mode.set("选择操作对象类型")
        list_mode_select = tk.OptionMenu(page, accounts_listbox_mode, "students", "teachers", "admins",
                                         command=lambda x: self.admin_logic.update_account_listbox(accounts_listbox,
                                                                                                   accounts_listbox_mode.get()))
        list_mode_select.grid(row=1, column=1, padx=10, pady=10)

        confirm_button = tk.Button(page, text="确认操作对象", state=STATE[1], **button_normal_style,
                                   command=lambda: self.admin_logic.confirm_object(accounts_listbox, mode="accounts",
                                                                                   add_button=add_button,
                                                                                   accounts_listbox_mode=accounts_listbox_mode,
                                                                                   choose_object=choose_object,
                                                                                   confirm_id=confirm_id,
                                                                                   confirm_button=confirm_button,
                                                                                   state=STATE,
                                                                                   delete_button=delete_button,
                                                                                   reset_button=reset_button,
                                                                                   confirm_id_entry=confirm_id_entry,
                                                                                   confirm_username_entry=confirm_username_entry,
                                                                                   button_normal_style=button_normal_style,
                                                                                   button_disabled_style=button_disabled_style
                                                                                   ))

        confirm_button.grid(row=2, column=1, padx=10, pady=10)

        # 确认操作对象区
        choose_object = tk.StringVar()
        choose_object.set("选择操作对象类型")
        choose_entry = tk.Entry(page, textvariable=choose_object, state=STATE[0])
        choose_entry.grid(row=1, column=0, padx=10, pady=10)

        # ID确定区
        confirm_id = tk.StringVar()
        confirm_id.set("待操作对象ID")
        confirm_id_entry = tk.Entry(page, textvariable=confirm_id)
        confirm_id_entry.grid(row=2, column=0, padx=10, pady=10)

        # 用户名确定区
        confirm_username = tk.StringVar()
        confirm_username.set("用户名")
        confirm_username_entry = tk.Entry(page, textvariable=confirm_username, state=STATE[0])
        confirm_username_entry.grid(row=3, column=1, padx=10, pady=10)

        # Password确定区
        confirm_password = tk.StringVar()
        confirm_password.set("新密码")
        confirm_password_entry = tk.Entry(page, textvariable=confirm_password)
        confirm_password_entry.grid(row=3, column=0, padx=10, pady=10)

        # 添加账号按钮
        add_button = tk.Button(page, text="添加", state=STATE[0], **button_disabled_style,
                               command=lambda: self.admin_logic.add_accounts(accounts_listbox_mode.get(),
                                                                             confirm_id.get(),
                                                                             confirm_username.get(),
                                                                             confirm_password.get(),
                                                                             add_button=add_button,
                                                                             listbox=accounts_listbox,
                                                                             confirm_username=confirm_username,
                                                                             accounts_listbox_mode=accounts_listbox_mode,
                                                                             choose_object=choose_object,
                                                                             confirm_id=confirm_id,
                                                                             confirm_button=confirm_button,
                                                                             state=STATE,
                                                                             confirm_password=confirm_password,
                                                                             delete_button=delete_button,
                                                                             reset_button=reset_button,
                                                                             confirm_id_entry=confirm_id_entry,
                                                                             confirm_username_entry=confirm_username_entry,
                                                                             button_normal_style=button_normal_style,
                                                                             button_disabled_style=button_disabled_style
                                                                             ))
        add_button.grid(row=7, column=0, padx=10, pady=10)

        # 删除账号按钮
        delete_button = tk.Button(page, text="删除", state=STATE[0], **button_disabled_style,
                                  command=lambda: self.admin_logic.delete_accounts(accounts_listbox_mode.get(),
                                                                                   confirm_id.get(),
                                                                                   add_button=add_button,
                                                                                   listbox=accounts_listbox,
                                                                                   confirm_username=confirm_username,
                                                                                   accounts_listbox_mode=accounts_listbox_mode,
                                                                                   choose_object=choose_object,
                                                                                   confirm_id=confirm_id,
                                                                                   confirm_button=confirm_button,
                                                                                   state=STATE,
                                                                                   confirm_password=confirm_password,
                                                                                   delete_button=delete_button,
                                                                                   reset_button=reset_button,
                                                                                   confirm_id_entry=confirm_id_entry,
                                                                                   confirm_username_entry=confirm_username_entry,
                                                                                   button_normal_style=button_normal_style,
                                                                                   button_disabled_style=button_disabled_style
                                                                                   ))
        delete_button.grid(row=4, column=0, padx=10, pady=10)

        # 修改密码按钮
        reset_button = tk.Button(page, text="重置密码", state=STATE[0], **button_disabled_style,
                                 command=lambda: self.admin_logic.reset_password(accounts_listbox_mode.get(),
                                                                                 confirm_id.get(),
                                                                                 confirm_password.get(),
                                                                                 add_button=add_button,
                                                                                 listbox=accounts_listbox,
                                                                                 confirm_username=confirm_username,
                                                                                 accounts_listbox_mode=accounts_listbox_mode,
                                                                                 choose_object=choose_object,
                                                                                 confirm_id=confirm_id,
                                                                                 confirm_button=confirm_button,
                                                                                 state=STATE,
                                                                                 confirm_password=confirm_password,
                                                                                 delete_button=delete_button,
                                                                                 reset_button=reset_button,
                                                                                 confirm_id_entry=confirm_id_entry,
                                                                                 confirm_username_entry=confirm_username_entry,
                                                                                 button_normal_style=button_normal_style,
                                                                                 button_disabled_style=button_disabled_style
                                                                                 ))
        reset_button.grid(row=5, column=0, padx=10, pady=10)

        # 重新操作按钮
        reoperate_button = tk.Button(page, text="重新操作",  **button_normal_style,
                                     command=lambda: self.admin_logic.reoperate(add_button=add_button,
                                                                                listbox=accounts_listbox,
                                                                                confirm_username=confirm_username,
                                                                                accounts_listbox_mode=accounts_listbox_mode,
                                                                                choose_object=choose_object,
                                                                                confirm_id=confirm_id,
                                                                                confirm_button=confirm_button,
                                                                                state=STATE,
                                                                                confirm_password=confirm_password,
                                                                                delete_button=delete_button,
                                                                                reset_button=reset_button,
                                                                                confirm_id_entry=confirm_id_entry,
                                                                                confirm_username_entry=confirm_username_entry,
                                                                                button_normal_style=button_normal_style,
                                                                                button_disabled_style=button_disabled_style))
        reoperate_button.grid(row=6, column=0, padx=10, pady=10)

    def operate_config(self):
        """
        管理配置文件界面
        :return:
        """
        page = tk.Toplevel(self.window)
        page.title("管理配置文件")
        page.geometry("1000x600")

        button_style = {"font": ("Arial", 12), "bg": "#3498db", "fg": "white", "relief": tk.RAISED}

        confirm_key = tk.StringVar()
        confirm_key.set("待操作对象ID")
        confirm_value = tk.StringVar()
        confirm_value.set("新值")
        listbox = tk.Listbox(page)
        listbox.grid(row=0, column=0, padx=10, pady=10)

        confirm_button = tk.Button(page, text="确认操作对象", **button_style,
                                   command=lambda: self.admin_logic.confirm_object(listbox, mode="configs",
                                                                                   confirm_key=confirm_key))
        confirm_button.grid(row=1, column=0, padx=10, pady=10)

        confirm_key_entry = tk.Entry(page, textvariable=confirm_key)
        confirm_key_entry.grid(row=1, column=1, padx=10, pady=10)

        confirm_value_entry = tk.Entry(page, textvariable=confirm_value)
        confirm_value_entry.grid(row=1, column=2, padx=10, pady=10)

        change_button = tk.Button(page, text="修改", **button_style,
                                  command=lambda: self.admin_logic.change_config(confirm_key.get(),
                                                                                 confirm_value.get()))
        change_button.grid(row=2, column=0, padx=10, pady=10)

        reoperate_button = tk.Button(page, text="刷新", **button_style,
                                     command=lambda: self.admin_logic.update_config_listbox(listbox))
        reoperate_button.grid(row=6, column=0, padx=10, pady=10)

    def register_courses(self):
        """
        开通课程界面
        :return:
        """
        page = tk.Toplevel(self.window)
        page.title("开通课程")
        notebook = ttk.Notebook(page)

        times = [str(item) for item in range(1, 13)]
        checkboxes = {}
        n = self.admin_logic.get_week_num()
        for i in range(n):
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=f"Week {i + 1}")

            for j in range(5):
                date_label = ttk.Label(frame, text="Monday Tuesday Wednesday Thursday Friday".split()[j])
                date_label.grid(row=0, column=j)

                for idx, time in enumerate(times):
                    var = tk.IntVar()
                    checkbox = ttk.Checkbutton(frame, text=time, variable=var)
                    checkbox.grid(row=idx + 1, column=j)
                    checkboxes[str(i + 1) + " " + str(j + 1) + " " + time] = var

        other_frame = ttk.Frame(notebook)
        notebook.add(other_frame, text="其他信息")

        id_label = ttk.Label(other_frame, text="课程ID")
        id_label.pack()
        id_entry = ttk.Entry(other_frame)
        id_entry.pack()
        name_label = ttk.Label(other_frame, text="课程名")
        name_label.pack()
        name_entry = ttk.Entry(other_frame)
        name_entry.pack()
        term_label = ttk.Label(other_frame, text="学期")
        term_label.pack()
        term_entry = ttk.Entry(other_frame)
        term_entry.pack()
        teacher_id_label = ttk.Label(other_frame, text="教师ID")
        teacher_id_label.pack()
        teacher_id_entry = ttk.Entry(other_frame)
        teacher_id_entry.pack()
        notebook.pack()

        btn = tk.Button(page, text="Submit",
                        command=lambda: self.admin_logic.confirm_register_course(checkboxes, id=id_entry.get(),
                                                                                 name=name_entry.get(),
                                                                                 term=term_entry.get(),
                                                                                 teacher_id=teacher_id_entry.get()))
        btn.pack()

    def delete_courses(self):
        """
        删除课程界面
        :return:
        """
        page = tk.Toplevel(self.window)
        page.title("删除课程")
        page.geometry("1000x600")

        button_style = {"font": ("Arial", 12), "bg": "#3498db", "fg": "white", "relief": tk.RAISED}

        listbox = tk.Listbox(page)
        listbox.grid(row=0, column=0, padx=10, pady=10)

        self.admin_logic.update_course_listbox(listbox)

        confirm_button = tk.Button(page, text="确认操作对象", **button_style,
                                   command=lambda: self.admin_logic.confirm_object(listbox, mode="courses",
                                                                                   confirm_id=confirm_id))
        confirm_button.grid(row=1, column=0, padx=10, pady=10)

        confirm_id = tk.StringVar()
        confirm_id.set("待操作对象ID")
        confirm_id_entry = tk.Entry(page, textvariable=confirm_id)
        confirm_id_entry.grid(row=1, column=1, padx=10, pady=10)

        delete_button = tk.Button(page, text="删除", **button_style,
                                  command=lambda: self.admin_logic.delete_courses(confirm_id.get()))
        delete_button.grid(row=2, column=0, padx=10, pady=10)

    def initialize_page(self):
        """
        初始化数据界面
        :return:
        """
        page = tk.Toplevel(self.window)
        page.title("初始化数据")
        page.geometry("400x100")
        page.resizable(0, 0)

        code_label = tk.Label(page, text="请输入确认码")
        code_label.pack()
        code_entry = tk.Entry(page)
        code_entry.pack()
        confirm_button = tk.Button(page, text="确认", command=lambda: self.admin_logic.confirm_init(code_entry.get()))
        confirm_button.pack()
