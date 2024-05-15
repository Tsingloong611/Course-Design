# @File: student.py
import tkinter as tk
from tkinter import messagebox, filedialog
from dao.tools import *


class StudentLogic:
    def __init__(self):
        pass

    # 冲突课程检测
    def check_conflict(self, course1_id, course2_id):
        """
        检测两门课程是否有时间冲突
        :param course1_id: 第一门课程的id
        :param course2_id: 第二门课程的id
        :return: 若冲突，返回True，否则返回False
        """
        course1 = tools().load_data(type="courses", id=course1_id)
        course2 = tools().load_data(type="courses", id=course2_id)
        if course1["term"] == course2["term"]:
            for i in course1["time"]:
                for j in course2["time"]:
                    if i["week"] == j["week"] and i["day"] == j["day"]:
                        for m in i["time"]:
                            for n in j["time"]:
                                if m == n:
                                    return True
        return False

    # 选课

    def enroll_course(self, student_id, course_id):
        """
        选课
        :param student_id: 学生id
        :param course_id: 课程id
        :return: 若选课成功，返回True，否则返回False
        """
        students = tools().load_data(type="students")
        student = tools().load_data(type="students", id=student_id)
        courses = tools().load_data(type="courses")
        course = tools().load_data(type="courses", id=course_id)
        new_course = {"course_id": course_id,
                      "grade": "Not Graded"}
        if not course:
            messagebox.showerror("错误", "选课失败，课程不存在")
            return False
        elif student_id in course["student_ids"]:
            messagebox.showerror("错误", "选课失败，已选过该课程")
            return False
        else:
            for i in courses:
                if student_id in i["student_ids"]:
                    print(i)
                    if self.check_conflict(i["id"], course_id):
                        messagebox.showerror("错误", "选课失败，与已选课程时间冲突")
                        return False
            course["student_ids"].append(student_id)
            student["enrolled_courses"].append(new_course)
            for i in range(len(courses)):
                if courses[i]["id"] == course_id:
                    courses[i] = course
                    break
            tools().save_data(type="courses", new_datas=courses)
            for i in range(len(students)):
                if students[i]["id"] == student_id:
                    students[i] = student
                    break
            tools().save_data(type="students", new_datas=students)
            messagebox.showinfo("成功", "选课成功")
            return True

    # 退课
    def exit_course(self, student_id, course_id):
        """
        退课
        :param student_id: 学生id
        :param course_id: 课程id
        :return: 若退课成功，返回True，否则返回False
        """
        students = tools().load_data(type="students")
        student = tools().load_data(type="students", id=student_id)
        courses = tools().load_data(type="courses")
        course = tools().load_data(type="courses", id=course_id)
        if not course:
            messagebox.showerror("错误", "退课失败，课程不存在")
            return False
        elif student_id not in course["student_ids"]:
            messagebox.showerror("错误", "退课失败，未选过该课程")
            return False
        else:
            course["student_ids"] = [i for i in course["student_ids"] if i != student_id]
            for i in range(len(courses)):
                if courses[i]["id"] == course_id:
                    courses[i] = course
                    break
            tools().save_data(type="courses", new_datas=courses)
            student["enrolled_courses"] = [i for i in student["enrolled_courses"] if i["course_id"] != course_id]
            for i in range(len(students)):
                if students[i]["id"] == student_id:
                    students[i] = student
                    break
            tools().save_data(type="students", new_datas=students)
            messagebox.showinfo("成功", "退课成功")
            return True

    def update_course_listbox(self, listbox, student_id, term, mode):
        listbox.delete(0, tk.END)
        keys = tools().load_data("statement")["course_attributes"]

        if term != "all":
            courses = [course for course in tools().load_data("courses") if course["term"] == term]
        else:
            courses = [course for course in tools().load_data("courses")]

        statement_str = "".join("{:<20}".format(key) for key in keys) + "{:<20}".format("teacher_name")

        if mode == "enroll":
            lst = [i for i in courses if student_id not in i["student_ids"]]
            listbox.insert(0, statement_str)
            for item in lst:
                teacher_id = item["teacher_id"]
                teacher_name = tools().get_info(type="teachers", id=teacher_id, mode="username")
                row_str = "".join("{:<20}".format(item[key]) for key in keys) + "{:<20}".format(teacher_name)
                listbox.insert(tk.END, row_str)

        elif mode == "exit":
            lst = [i for i in courses if student_id in i["student_ids"]]
            listbox.insert(0, statement_str)
            for item in lst:
                teacher_id = item["teacher_id"]
                teacher_name = tools().get_info(type="teachers", id=teacher_id, mode="username")
                row_str = "".join("{:<20}".format(item[key]) for key in keys) + "{:<20}".format(teacher_name)
                listbox.insert(tk.END, row_str)

        elif mode == "grade":
            lst = [i for i in courses if student_id in i["student_ids"]]
            statement_str = statement_str + "{:<20}".format("grade")
            listbox.insert(0, statement_str)
            student_courses = tools().load_data(type="students", id=student_id)["enrolled_courses"]
            for item in lst:
                grade = ""
                course_id = item["id"]
                teacher_id = item["teacher_id"]
                teacher_name = tools().get_info(type="teachers", id=teacher_id, mode="username")
                for course in student_courses:
                    if course["course_id"] == course_id:
                        grade = course["grade"]
                row_str = "".join("{:<20}".format(item[key]) for key in keys) + "{:<20}{:<20}".format(teacher_name,
                                                                                                      grade)
                listbox.insert(tk.END, row_str)

        max_length = max(len(row_str) for row_str in listbox.get(0, tk.END))
        listbox.config(width=max_length)

    def confirm_object(self, listbox, mode, **kwargs):
        STATE = kwargs.get("state", None)
        if mode == "course_center":
            confirm_id = kwargs.get("confirm_id", None)
            submit_assignment_button = kwargs.get("submit_assignment_button", None)
            show_grade_button = kwargs.get("show_grade_button", None)
            discussion_forum_button = kwargs.get("discussion_forum_button", None)
            show_material_button = kwargs.get("show_material_button", None)
            if confirm_id.get() == "待操作对象ID":
                if listbox.curselection():
                    if self.get_object(listbox)[0] not in ["id"]:
                        confirm_id.set(self.get_object(listbox)[0])
                        submit_assignment_button.config(state=STATE[1])
                        show_grade_button.config(state=STATE[1])
                        discussion_forum_button.config(state=STATE[1])
                        show_material_button.config(state=STATE[1])
                    else:
                        messagebox.showwarning("警告", "请正确选择列表内容作为操作对象!")
                else:
                    messagebox.showwarning("警告", "请从列表选取对象或者手动指定对象ID")
            elif confirm_id.get() != "待操作对象ID" and listbox.curselection():
                if self.get_object(listbox)[0] not in ["id"]:
                    confirm_id.set(self.get_object(listbox)[0])
                    submit_assignment_button.config(state=STATE[1])
                    show_grade_button.config(state=STATE[1])
                    discussion_forum_button.config(state=STATE[1])
                else:
                    messagebox.showwarning("警告", "请正确选择列表内容作为操作对象!")



        elif mode == "enroll_course" or mode == "exit_course":
            confirm_id = kwargs.get("confirm_id", None)
            if confirm_id.get() == "待操作对象ID":
                if listbox.curselection():
                    if self.get_object(listbox)[0] not in ["id"]:
                        confirm_id.set(self.get_object(listbox)[0])
                    else:
                        messagebox.showwarning("警告", "请正确选择列表内容作为操作对象!")
                else:
                    messagebox.showwarning("警告", "请从列表选取对象或者手动指定对象ID")
            elif confirm_id.get() != "待操作对象ID" and listbox.curselection():
                if self.get_object(listbox)[0] not in ["id"]:
                    confirm_id.set(self.get_object(listbox)[0])
                else:
                    messagebox.showwarning("警告", "请正确选择列表内容作为操作对象!")

    def get_object(self, listbox):
        return str(listbox.get(listbox.curselection())).split()

    def update_course_schedule(self, student_id, selected_term, selected_week, labels, page):
        courses = [course for course in tools().load_data(type="courses") if student_id in course["student_ids"]]
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

    def submit_assignment(self, student_id, course_id):
        assignment_path = filedialog.askopenfilename()
        directory = rf"./data/materials_data/{course_id}/homeworks/{student_id}/"
        tools().check_dir(directory)
        shutil.copy(assignment_path, directory)
        messagebox.showinfo("上传", f"已将{assignment_path}上传至{directory}")

    def show_grade(self, student_id, course_id):
        student = tools().load_data(type="students", id=student_id)
        for course in student["enrolled_courses"]:
            if course["course_id"] == course_id:
                student_name = student["username"]
                student_grade = course["grade"]
                messagebox.showinfo("查询结果", f"{student_name}的课程{course_id}的成绩是{student_grade}")

    def get_week_num(self):
        return int(tools().load_config()["week_num"])

    def get_name(self, student_id):
        return tools().get_info(type="students", id=student_id, mode="username")

    def show_materials(self, course_id):
        directory_path = fr'.\data\materials_data\{course_id}\materials'
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        os.startfile(directory_path)