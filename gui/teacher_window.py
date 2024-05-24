# @File: teacher_window.py
import tkinter as tk

from gui.discussion_forum_window import DiscussionForumWindow
from logic.teacher import TeacherLogic


class TeacherWindow:
    def __init__(self):
        pass

    def __init__(self, root, teacher_id):
        """
        教师界面
        :param root: 窗口
        :param teacher_id: 教师id
        """
        self.teacher_logic = TeacherLogic()
        self.teacher_id = teacher_id
        self.window = root
        self.window.title(f"欢迎教师 {self.teacher_logic.get_name(teacher_id)}")
        self.window.geometry("300x100")
        self.window.resizable(False, False)

        button_style = {"font": ("Arial", 12), "bg": "#3498db", "fg": "white", "relief": tk.RAISED}

        self.show_course_button = tk.Button(self.window, text="查课表", command=self.show_course_page, **button_style)
        self.show_course_button.pack(pady=10)

        self.course_center_button = tk.Button(self.window, text="课程中心", command=self.course_center_page,
                                              **button_style)
        self.course_center_button.pack(pady=10)

    def show_course_page(self):
        """
        展示课表
        :return:
        """
        page = tk.Toplevel(self.window)
        page.title("展示课表")
        page.geometry("1000x600")

        # 优化样式和布局
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
        n = self.teacher_logic.get_week_num()
        weeks = [f"Week {i + 1}" for i in range(n)]
        selected_week = tk.StringVar()
        selected_week.set(weeks[0])

        week_dropdown = tk.OptionMenu(page, selected_week, *weeks)
        week_dropdown.grid(row=0, column=3)

        term_label = tk.Label(page, text="选择学期:", **label_style)
        term_label.grid(row=0, column=0)

        terms = self.teacher_logic.get_terms()
        selected_term = tk.StringVar()
        selected_term.set(terms[0])

        term_dropdown = tk.OptionMenu(page, selected_term, *terms)
        term_dropdown.grid(row=0, column=1)

        labels = []

        update_button = tk.Button(page, text="更新",
                                  command=lambda: self.teacher_logic.update_course_schedule(teacher_id=self.teacher_id,
                                                                                            selected_term=selected_term,
                                                                                            selected_week=selected_week,
                                                                                            labels=labels, page=page),
                                  **button_style)
        update_button.grid(row=0, column=5)

    def course_center_page(self):
        """
        课程中心
        :return:
        """
        page = tk.Toplevel(self.window)
        page.title("课程中心")
        page.geometry("1000x1000")

        STATE = ["disabled", "normal"]

        label_style = {"font": ("Arial", 12)}
        button_normal_style = {"font": ("Arial", 12), "bg": "#3498db", "fg": "white", "relief": tk.RAISED}
        button_disabled_style = {"font": ("Arial", 12), "bg": "#bdc3c7", "fg": "#7f8c8d", "relief": tk.FLAT}

        term_label = tk.Label(page, text="选择学期:", **label_style)
        term_label.grid(row=0, column=0)

        terms = self.teacher_logic.get_terms()
        selected_term = tk.StringVar()
        selected_term.set(terms[0])

        term_dropdown = tk.OptionMenu(page, selected_term, *terms)
        term_dropdown.grid(row=0, column=1)

        update_list_button = tk.Button(page, text="确定学期", **button_normal_style,
                                       command=lambda: self.teacher_logic.update_course_listbox(listbox,
                                                                                                teacher_id=self.teacher_id,
                                                                                                term=selected_term.get(),
                                                                                                ))
        update_list_button.grid(row=0, column=2)

        listbox = tk.Listbox(page)
        listbox.grid(row=1, column=0, padx=10, pady=10)


        course_label = tk.Label(page, text="选择课程:", **label_style)
        course_label.grid(row=2, column=0)
        confirm_button = tk.Button(page, text="确认课程", **button_normal_style,
                                   command=lambda: self.teacher_logic.confirm_object(listbox, listbox_two,
                                                                                     state=STATE,
                                                                                     confirm_id=confirm_id,
                                                                                     upload_materials_button=upload_materials_button,
                                                                                     discussion_forum_button=discussion_forum_button,
                                                                                     show_material_button=show_material_button,
                                                                                     button_normal_style=button_normal_style,
                                                                                     button_disabled_style=button_disabled_style))
        confirm_button.grid(row=2, column=2, padx=10, pady=10)

        confirm_id = tk.StringVar()
        confirm_id.set("待操作课程ID")
        confirm_id_entry = tk.Entry(page, textvariable=confirm_id, state=STATE[0])
        confirm_id_entry.grid(row=2, column=1, padx=10, pady=10)

        show_material_button = tk.Button(page, text="查看资料", state=STATE[0], **button_disabled_style,
                                         command=lambda: self.teacher_logic.show_materials(course_id=confirm_id.get()))
        show_material_button.grid(row=3, column=1, padx=10, pady=10)

        upload_materials_button = tk.Button(page, text="上传资料", state=STATE[0], **button_disabled_style,
                                            command=lambda: self.teacher_logic.upload_materials(course_id=
                                                                                                confirm_id.get()))
        upload_materials_button.grid(row=3, column=0, padx=10, pady=10)

        show_homework_button = tk.Button(page, text="查看作业", state=STATE[0], **button_disabled_style,
                                         command=lambda: self.teacher_logic.show_assignment(
                                             course_id=confirm_id.get()
                                             , student_id=confirm_two_id.get()))

        show_homework_button.grid(row=6, column=0, padx=10, pady=10)

        discussion_forum_button = tk.Button(page, text="讨论区", state=STATE[0], **button_disabled_style,
                                            command=lambda: DiscussionForumWindow(tk.Toplevel(page),
                                                                                  course_id=confirm_id.get(),
                                                                                  name=self.teacher_logic.get_name(
                                                                                      self.teacher_id),
                                                                                  type="Teacher"))
        discussion_forum_button.grid(row=3, column=2, padx=10, pady=10)

        listbox_two = tk.Listbox(page)
        listbox_two.grid(row=5, column=0, padx=10, pady=10)

        update_list_button = tk.Button(page, text="确定学生", **button_normal_style,
                                       command=lambda: self.teacher_logic.confirm_student(listbox_two, confirm_two_id,
                                                                                          show_homework_button,
                                                                                          mark_button,
                                                                                          button_normal_style))
        update_list_button.grid(row=4, column=2)

        grade = tk.StringVar()
        grade.set("输入分数")
        mark_entry = tk.Entry(page, textvariable=grade)
        mark_entry.grid(row=6, column=1, padx=10, pady=10)

        student_label = tk.Label(page, text="选择学生：", **label_style)
        student_label.grid(row=4, column=0)

        confirm_two_id = tk.StringVar()
        confirm_two_id.set("待操作学生ID")
        confirm_two_id_entry = tk.Entry(page, textvariable=confirm_two_id, state=STATE[0])
        confirm_two_id_entry.grid(row=4, column=1, padx=10, pady=10)

        mark_button = tk.Button(page, text="打分", state=STATE[0], **button_disabled_style,
                                command=lambda: self.teacher_logic.mark_grade(course_id=confirm_id.get(),
                                                                              student_id=confirm_two_id.get(),
                                                                              grade=grade.get()))
        mark_button.grid(row=6, column=2, padx=10, pady=10)
