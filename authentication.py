# @File: authentication.py
from tools import *


class AuthenticationLogic:
    def __init__(self):
        pass

    def login(self, input_id, input_password, mode):
        datas = tools().get_accounts(mode)
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

    statement= {
            "attributes": [ "id", "username", "password"]
    }
    students = [
        { "id": "123456", "username": "student_test", "password": "123456"}
    ]

    teachers = [
        { "id": "123456", "username": "teacher_test", "password": "123456"}
    ]

    admins = [
        { "id": "123456", "username": "admin_test", "password": "123456"}
    ]

    accounts = {"statement": statement, "students": students, "teachers": teachers, "admins": admins}
    with open("./data/accounts_data.json", "w") as f:
        json.dump(accounts, f, indent=4)

    authentication_logic = AuthenticationLogic()
    authentication_logic.login("123456", "123456", "students")
