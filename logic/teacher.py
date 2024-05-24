# @File: teacher.py
from tkinter import filedialog

from dao.tools import *
import tkinter as tk


class TeacherLogic:
    def __init__(self):
        pass

    def update_course_listbox(self, listbox, teacher_id, term):
        """
        更新课程列表框
        :param listbox: 列表框
        :param teacher_id: 用户id
        :param term: 学期
        :return:
        """
        listbox.delete(0, tk.END)
        keys = tools().load_data("statements")["course_attributes"]
        courses = [course for course in tools().load_data(type="courses") if
                   course["teacher_id"] == teacher_id and course["term"] == term]
        statement_str = "".join("{:<20}".format(key) for key in keys)
        listbox.insert(0, statement_str)
        for item in courses:
            row_str = "".join("{:<20}".format(item[key]) for key in keys)
            listbox.insert(tk.END, row_str)
        max_length = max(len(row_str) for row_str in listbox.get(0, tk.END))
        listbox.config(width=max_length)

    def update_student_listbox(self, listbox, course_id):
        """
        更新学生列表框
        :param listbox: 列表框
        :param course_id: 课程id
        :return:
        """
        listbox.delete(0, tk.END)
        keys = ["id", "name", "grade"]
        statement_str = "".join("{:<20}".format(key) for key in keys)
        listbox.insert(0, statement_str)
        course = tools().load_data(type="courses", id=course_id)
        student_ids = course["student_ids"]
        for id in student_ids:
            student = tools().load_data(type="students", id=id)
            student_name = student["username"]
            for item in student["enrolled_courses"]:
                if item["course_id"] == course_id:
                    student_grade = item["grade"]
                    break
            row_str = "{:<20}{:<20}{:<20}".format(id, student_name, student_grade)
            listbox.insert(tk.END, row_str)
        max_length = max(len(row_str) for row_str in listbox.get(0, tk.END))
        listbox.config(width=max_length)

    def update_course_schedule(self, teacher_id, selected_term, selected_week, labels, page):
        """
        更新课程表
        :param teacher_id: 用户id
        :param selected_term: 学期
        :param selected_week: 周
        :param labels: 标签
        :param page: 页面
        :return:
        """
        courses = [course for course in tools().load_data(type="courses") if course["teacher_id"] == teacher_id]
        selected_week = selected_week.get().split()[1]
        selected_term = selected_term.get()
        for label in labels:
            label.grid_remove()
        labels.clear()
        for course in courses:
            term = course["term"]
            if term == selected_term:
                for class_time in course["time"]:
                    week = int(class_time["week"])
                    day = int(class_time["day"])
                    times = class_time["time"]
                    course_info = f"{course['name']}\nRoom: {course['room']}"
                    for time in times:
                        if week == int(selected_week):
                            label = tk.Label(page, text=course_info, borderwidth=1, relief="solid", padx=10, pady=5)
                            label.grid(row=int(time) + 1, column=day)
                            labels.append(label)

    def confirm_object(self, listbox, listbox_two, **kwargs):
        """
        确认操作对象
        :param listbox: 列表框一
        :param listbox_two: 列表框二
        :param kwargs: 组件状态参数
        :return:
        """

        STATE = kwargs.get("state", None)
        if listbox.curselection():
            if self.get_object(listbox)[0] not in ["id"]:
                confirm_id = kwargs.get("confirm_id", None)

                upload_materials_button = kwargs.get("upload_materials_button", None)
                discussion_forum_button = kwargs.get("discussion_forum_button", None)
                show_material_button = kwargs.get("show_material_button", None)
                button_normal_style = kwargs.get("button_normal_style", None)
                button_disabled_style = kwargs.get("button_disabeld_style", None)

                confirm_id.set(self.get_object(listbox)[0])

                upload_materials_button.config(state=STATE[1], **button_normal_style)
                discussion_forum_button.config(state=STATE[1], **button_normal_style)
                show_material_button.config(state=STATE[1], **button_normal_style)
                self.update_student_listbox(listbox=listbox_two, course_id=confirm_id.get())
            else:
                messagebox.showwarning("警告", "请正确选择列表内容作为操作对象!")
        else:
            messagebox.showwarning("警告", "请选择操作对象!")

    def confirm_student(self, listbox_two, confirm_two_id, show_homework_button, mark_button, button_normal_style):
        """
        确认学生
        :param listbox_two: 列表框二
        :param confirm_two_id: 学生id
        :param show_homework_button: 组件状态参数
        :param button_normal_style: 样式
        :return:
        """
        if listbox_two.curselection():
            if self.get_object(listbox_two)[0] not in ["id"]:
                confirm_two_id.set(self.get_object(listbox_two)[0])
                mark_button.config(state="normal", **button_normal_style)
                show_homework_button.config(state="normal", **button_normal_style)
            else:
                messagebox.showwarning("警告", "请正确选择列表内容作为操作对象!")
        else:
            messagebox.showwarning("警告", "请选择操作对象!")

    def get_object(self, listbox):
        """
        获取列表框中的对象
        :param listbox: 列表框
        :return: 返回列表框中的对象的字符串分割后的列表
        """
        return str(listbox.get(listbox.curselection())).split()

    def upload_materials(self, course_id):
        """
        上传教学资料
        :param course_id: 课程id
        :return:
        """
        file_path = filedialog.askopenfilename()
        directory = rf"./data/materials_data/{course_id}/materials/"
        tools().check_dir(directory)
        shutil.copy(file_path, directory)
        messagebox.showinfo("上传", f"已将{file_path}上传至{directory}")

    def mark_grade(self, course_id, student_id, grade):
        """
        打分
        :param course_id: 课程id
        :param student_id: 学生id
        :param grade: 分数
        :return:
        """
        students = tools().load_data(type="students")

        for student in students:
            if student["id"] == student_id:
                courses = student["enrolled_courses"]
                for course in courses:
                    if course["course_id"] == course_id:
                        course["grade"] = grade
                        course_name = tools().get_info("courses", course_id, "name")
                        student_name = tools().get_info("students", student_id)
                        messagebox.showinfo("打分成功", f"课程 {course_name} 中学生 {student_name} 的分数已设置为 {grade}")
                        break

                # 保存更新后的学生数据
                tools().save_data(type="students", new_datas=students)
                break


    def show_assignment(self, course_id, student_id):
        """
        查看作业
        :param course_id: 课程id
        :param student_id: 学生id
        :return: 调用任务资源管理器打开对应学生的作业文件夹
        """
        directory_path = fr'.\data\materials_data\{course_id}\homeworks\{student_id}'
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        os.startfile(directory_path)

    def get_week_num(self):
        """
        获取周数
        :return: 返回 int类型的周数
        """
        return int(tools().load_config()["week_num"])

    def get_name(self, teacher_id):
        """
        获取教师姓名
        :param teacher_id: 教师id
        :return: str类型的教师姓名
        """
        return tools().get_info(type="teachers", id=teacher_id)

    def show_materials(self, course_id):
        """
        查看资料
        :param course_id: 课程id
        :return: 调用任务资源管理器打开对应课程的资料文件夹
        """
        directory_path = fr'.\data\materials_data\{course_id}\materials'
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        os.startfile(directory_path)

    def get_terms(self):
        """
        获取学期名
        :return: 学期列表
        """
        return tools().load_data("statements")["term_names"]
