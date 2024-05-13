# @File: teacher.py
from tkinter import filedialog

from tools import *
import tkinter as tk


class TeacherLogic:
    def __init__(self):
        pass

    def update_course_listbox(self, listbox, teacher_id, term):
        listbox.delete(0, tk.END)
        keys = tools().load_data("statement")["course_attributes"]
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
                    course_info = f"{course['name']}\nTeacher: {course['teacher_id']}"
                    for time in times:
                        if week == int(selected_week):
                            label = tk.Label(page, text=course_info, borderwidth=1, relief="solid", padx=10, pady=5)
                            label.grid(row=int(time) + 1, column=day)
                            labels.append(label)

    def confirm_object(self, listbox, listbox_two, **kwargs):

        STATE = kwargs.get("state", None)
        if listbox.curselection():
            if self.get_object(listbox)[0] not in ["id"]:
                confirm_id = kwargs.get("confirm_id", None)

                upload_materials_button = kwargs.get("upload_materials_button", None)
                discussion_forum_button = kwargs.get("discussion_forum_button", None)

                confirm_id.set(self.get_object(listbox)[0])

                upload_materials_button.config(state=STATE[1])
                discussion_forum_button.config(state=STATE[1])
                self.update_student_listbox(listbox=listbox_two, course_id=confirm_id.get())
            else:
                messagebox.showwarning("警告", "请正确选择列表内容作为操作对象!")
        else:
            messagebox.showwarning("警告", "请选择操作对象!")

    def confirm_student(self, listbox_two, confirm_two_id,show_homework_button):
        if listbox_two.curselection():
            if self.get_object(listbox_two)[0] not in ["id"]:
                confirm_two_id.set(self.get_object(listbox_two)[0])
                show_homework_button.config(state="normal")
            else:
                messagebox.showwarning("警告", "请正确选择列表内容作为操作对象!")
        else:
            messagebox.showwarning("警告", "请选择操作对象!")

    def get_object(self, listbox):
        return str(listbox.get(listbox.curselection())).split()

    def upload_materials(self, teacher_id, course_id):
        file_path = filedialog.askopenfilename()
        directory = f"./data/materials_data/{course_id}/materials/"
        tools().check_dir(directory)
        shutil.copy(file_path, directory)
        messagebox.showinfo("上传", f"已将{file_path}上传至{directory}")

    def mark_grade(self, course_id, student_id, grade):
        students = tools().load_data(type="students")

        for student in students:
            if student["id"] == student_id:
                courses = student["enrolled_courses"]
                for course in courses:
                    if course["course_id"] == course_id:
                        course["grade"] = grade
                        break

                # 保存更新后的学生数据
                tools().save_data(type="students", new_datas=students)
                break

    def show_assignment(self, course_id, student_id):
        directory_path = fr'.\data\materials_data\{course_id}\homeworks\{student_id}'
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        os.startfile(directory_path)

