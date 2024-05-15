# @File: authentication.py
from dao.tools import *


class AuthenticationLogic:
    def __init__(self):
        pass

    def login(self, input_id, input_password, type):
        datas = tools().load_data(type)
        for data in datas:
            if data["id"] == input_id and data["password"] == input_password:
                return data


if __name__ == "__main__":
    '''
    Warning: Do not run this script in the production environment.
        This is a test case for the authentication logic.
        
    This will overwrite the original datas.json file, leading to data loss.
    This will overwrite the original datas.json file, leading to data loss.
    This will overwrite the original datas.json file, leading to data loss.
    '''
    import json

    statement = {
        "account_attributes": ["id", "username", "password"],
        "config_attributes": ["key", "value"],
        "course_attributes": ["id", "name", "term", "teacher_id"],
    }
    students = [
        {"id": "1", "username": "student_test", "password": "1",
         "enrolled_courses": [{"course_id": "0", "grade": "100"}]},
    ]

    teachers = [
        {"id": "1", "username": "teacher_test", "password": "1", "teaching_courses": [{"course_id": "0"}]}
    ]

    admins = [
        {"id": "1", "username": "admin_test", "password": "1"}
    ]

    courses = [{
        "id": "1",
        "name": "test_course",
        "term": "1",
        "time": [],
        "teacher_id": "1",
        "student_ids": []
    }]

    accounts = {"statement": statement, "students": students, "teachers": teachers, "admins": admins,
                "courses": courses}
    with open("./data/data.json", "w") as f:
        json.dump(accounts, f, indent=4)

    authentication_logic = AuthenticationLogic()
    authentication_logic.login("1", "1", "admins")
