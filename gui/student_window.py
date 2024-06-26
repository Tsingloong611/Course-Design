# @File: student_window.py
from gui.discussion_forum_window import DiscussionForumWindow
from logic.student import StudentLogic
import tkinter as tk


class StudentWindow:
    def __init__(self, root, student_id):
        """
        学生界面
        :param root: 窗口
        :param student_id: 学生id
        """
        self.student_logic = StudentLogic()
        self.STATE = ["disabled", "normal"]
        self.student_id = student_id
        self.window = root
        self.window.title(f"欢迎学生 {self.student_logic.get_name(student_id)}")
        self.window.geometry("300x300")
        self.window.resizable(False, False)


        button_style = {"font": ("Arial", 12), "bg": "#3498db", "fg": "white", "relief": tk.RAISED}

        self.enroll_course_button = tk.Button(self.window, text="选课", command=self.enroll_course_page, **button_style)
        self.enroll_course_button.pack(pady=10)

        self.show_course_button = tk.Button(self.window, text="查课表", command=self.show_course_page, **button_style)
        self.show_course_button.pack(pady=10)

        self.exit_course_button = tk.Button(self.window, text="退课", command=self.exit_course_page, **button_style)
        self.exit_course_button.pack(pady=10)

        self.course_center_button = tk.Button(self.window, text="课程中心", command=self.course_center_page,
                                              **button_style)
        self.course_center_button.pack(pady=10)

        self.all_grade_button = tk.Button(self.window, text="成绩总表", command=self.all_grade_page, **button_style)
        self.all_grade_button.pack(pady=10)

    def enroll_course_page(self):
        """
        选课界面
        :return:
        """
        page = tk.Toplevel(self.window)
        page.title("加入课程")
        page.geometry("1000x600")

        # 优化样式和布局
        label_style = {"font": ("Arial", 12)}
        button_style = {"font": ("Arial", 12), "bg": "#3498db", "fg": "white", "relief": tk.RAISED}

        term_label = tk.Label(page, text="选择学期:", **label_style)
        term_label.grid(row=0, column=0)

        terms = self.student_logic.get_terms()
        selected_term = tk.StringVar()
        selected_term.set(terms[0])

        term_dropdown = tk.OptionMenu(page, selected_term, *terms)
        term_dropdown.grid(row=0, column=1)

        listbox = tk.Listbox(page)
        listbox.grid(row=1, column=0, padx=10, pady=10)

        update_list_button = tk.Button(page, text="确定学期",
                                       command=lambda: (
                                           self.student_logic.update_course_listbox(
                                               listbox,
                                               student_id=self.student_id,
                                               term=selected_term.get(),
                                               mode="enroll")), **button_style)
        update_list_button.grid(row=0, column=2)

        confirm_id = tk.StringVar()
        confirm_id.set("待操作对象ID")
        confirm_id_entry = tk.Entry(page, textvariable=confirm_id)
        confirm_id_entry.grid(row=3, column=1, padx=10, pady=10)

        confirm_button = tk.Button(page, text="确认操作对象",
                                   command=lambda: self.student_logic.confirm_object(listbox, mode="enroll_course",
                                                                                     confirm_id=confirm_id),
                                   **button_style)
        confirm_button.grid(row=2, column=0, padx=10, pady=10)

        delete_button = tk.Button(page, text="选课",
                                  command=lambda: self.student_logic.enroll_course(self.student_id, confirm_id.get()),
                                  **button_style)
        delete_button.grid(row=3, column=0, padx=10, pady=10)

    def show_course_page(self):
        """
        展示课表
        :return:
        """
        page = tk.Toplevel(self.window)
        page.title("展示课表")
        page.geometry("1000x600")

        label_style = {"font": ("Arial", 12)}
        button_style = {"font": ("Arial", 12), "bg": "#3498db", "fg": "white", "relief": tk.RAISED}

        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for i, day in enumerate(days_of_week):
            day_label = tk.Label(page, text=day, **label_style)
            day_label.grid(row=1, column=i + 1)

        times_of_day = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
        for i, time in enumerate(times_of_day):
            time_label = tk.Label(page, text=time, borderwidth=2, relief="solid", padx=10, pady=5, **label_style)
            time_label.grid(row=i + 2, column=0)

        week_label = tk.Label(page, text="选择周:", **label_style)
        week_label.grid(row=0, column=2)
        n = self.student_logic.get_week_num()
        weeks = [f"Week {i + 1}" for i in range(n)]
        selected_week = tk.StringVar()
        selected_week.set(weeks[0])

        week_dropdown = tk.OptionMenu(page, selected_week, *weeks)
        week_dropdown.grid(row=0, column=3)

        term_label = tk.Label(page, text="选择学期:", **label_style)
        term_label.grid(row=0, column=0)

        terms = self.student_logic.get_terms()
        selected_term = tk.StringVar()
        selected_term.set(terms[0])

        term_dropdown = tk.OptionMenu(page, selected_term, *terms)
        term_dropdown.grid(row=0, column=1)

        labels = []

        update_button = tk.Button(page, text="更新",
                                  command=lambda: self.student_logic.update_course_schedule(student_id=self.student_id,
                                                                                            selected_term=selected_term,
                                                                                            selected_week=selected_week,
                                                                                            labels=labels, page=page),
                                  **button_style)
        update_button.grid(row=0, column=5)

    def exit_course_page(self):
        """
        退课
        :return:
        """
        page = tk.Toplevel(self.window)
        page.title("退出课程")
        page.geometry("1000x600")

        label_style = {"font": ("Arial", 12)}
        button_style = {"font": ("Arial", 12), "bg": "#3498db", "fg": "white", "relief": tk.RAISED}

        term_label = tk.Label(page, text="选择学期:", **label_style)
        term_label.grid(row=0, column=0)

        terms = self.student_logic.get_terms()
        selected_term = tk.StringVar()
        selected_term.set(terms[0])

        term_dropdown = tk.OptionMenu(page, selected_term, *terms)
        term_dropdown.grid(row=0, column=1)

        listbox = tk.Listbox(page)
        listbox.grid(row=1, column=0, padx=10, pady=10)

        update_list_button = tk.Button(page, text="确定学期", **button_style,
                                       command=lambda: self.student_logic.update_course_listbox(listbox,
                                                                                                student_id=self.student_id,
                                                                                                term=selected_term.get(),
                                                                                                mode="exit"))
        update_list_button.grid(row=0, column=2)

        confirm_button = tk.Button(page, text="确认操作对象", **button_style,
                                   command=lambda: self.student_logic.confirm_object(listbox, mode="exit_course",
                                                                                     confirm_id=confirm_id))
        confirm_button.grid(row=2, column=0, padx=10, pady=10)

        confirm_id = tk.StringVar()
        confirm_id.set("待操作对象ID")
        confirm_id_entry = tk.Entry(page, textvariable=confirm_id)
        confirm_id_entry.grid(row=2, column=1, padx=10, pady=10)

        delete_button = tk.Button(page, text="退课", **button_style,
                                  command=lambda: self.student_logic.exit_course(self.student_id, confirm_id.get()))
        delete_button.grid(row=3, column=0, padx=10, pady=10)

    def course_center_page(self):
        """
        课程中心
        :return:
        """
        page = tk.Toplevel(self.window)
        page.title("课程中心")
        page.geometry("1000x600")

        label_style = {"font": ("Arial", 12)}
        button_normal_style = {"font": ("Arial", 12), "bg": "#3498db", "fg": "white", "relief": tk.RAISED}
        button_disabled_style = {"font": ("Arial", 12), "bg": "#bdc3c7", "fg": "#7f8c8d", "relief": tk.FLAT}

        term_label = tk.Label(page, text="选择学期:", **label_style)
        term_label.grid(row=0, column=0)

        terms = self.student_logic.get_terms()
        selected_term = tk.StringVar()
        selected_term.set(terms[0])

        term_dropdown = tk.OptionMenu(page, selected_term, *terms)
        term_dropdown.grid(row=0, column=1)

        update_list_button = tk.Button(page, text="确定学期", **button_normal_style,
                                       command=lambda: self.student_logic.update_course_listbox(listbox,
                                                                                                student_id=self.student_id,
                                                                                                term=selected_term.get(),
                                                                                                mode="exit"))
        update_list_button.grid(row=0, column=2)

        listbox = tk.Listbox(page)
        listbox.grid(row=1, column=0, padx=10, pady=10)

        course_label = tk.Label(page, text="选择课程:", **label_style)
        course_label.grid(row=2, column=0)
        confirm_id = tk.StringVar()
        confirm_id.set("待操作课程ID")
        confirm_id_entry = tk.Entry(page, textvariable=confirm_id, state=self.STATE[0])
        confirm_id_entry.grid(row=2, column=1, padx=10, pady=10)
        confirm_button = tk.Button(page, text="确认课程", **button_normal_style,
                                   command=lambda: self.student_logic.confirm_object(listbox, mode="course_center",
                                                                                     confirm_id=confirm_id,
                                                                                     state=self.STATE,
                                                                                     submit_assignment_button=submit_assignment_button,
                                                                                     show_grade_button=show_grade_button,
                                                                                     discussion_forum_button=discussion_forum_button,
                                                                                     show_material_button=show_material_button,
                                                                                     button_normal_style=button_normal_style,
                                                                                     button_disabled_styl=button_disabled_style))
        confirm_button.grid(row=2, column=2, padx=10, pady=10)

        show_material_button = tk.Button(page, text="查看资料", state=self.STATE[0], **button_disabled_style,
                                         command=lambda: self.student_logic.show_materials(course_id=confirm_id.get()))
        show_material_button.grid(row=3, column=1, padx=10, pady=10)

        submit_assignment_button = tk.Button(page, text="提交作业", state=self.STATE[0], **button_disabled_style,
                                             command=lambda: self.student_logic.submit_assignment(self.student_id,
                                                                                                  confirm_id.get()))
        submit_assignment_button.grid(row=4, column=0, padx=10, pady=10)

        show_grade_button = tk.Button(page, text="查看成绩", state=self.STATE[0], **button_disabled_style,
                                      command=lambda: self.student_logic.show_grade(self.student_id, confirm_id.get()))

        show_grade_button.grid(row=3, column=0, padx=10, pady=10)

        discussion_forum_button = tk.Button(page, text="讨论区", state=self.STATE[0], **button_disabled_style,
                                            command=lambda: DiscussionForumWindow(tk.Toplevel(page),
                                                                                  course_id=confirm_id.get(),
                                                                                  name=self.student_logic.get_name(
                                                                                      self.student_id),
                                                                                  type="Student"))
        discussion_forum_button.grid(row=3, column=2, padx=10, pady=10)

    def all_grade_page(self):
        """
        成绩总表
        :return:
        """
        page = tk.Toplevel(self.window)
        page.title("成绩总表")
        page.geometry("1200x800")

        label_style = {"font": ("Arial", 12)}
        button_style = {"font": ("Arial", 12), "bg": "#3498db", "fg": "white", "relief": tk.RAISED}

        listbox = tk.Listbox(page)
        listbox.grid(row=1, column=0, padx=10, pady=10)

        term_label = tk.Label(page, text="选择学期:", **label_style)
        term_label.grid(row=0, column=0)

        terms = self.student_logic.get_terms()
        selected_term = tk.StringVar()
        selected_term.set(terms[0])

        term_dropdown = tk.OptionMenu(page, selected_term, *terms)
        term_dropdown.grid(row=0, column=1)

        update_list_button = tk.Button(page, text="确定学期", **button_style,
                                       command=lambda: self.student_logic.update_course_listbox(listbox,
                                                                                                student_id=self.student_id,
                                                                                                term=selected_term.get(),
                                                                                                mode="grade"))
        update_list_button.grid(row=0, column=2)
