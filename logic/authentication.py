# @File: authentication.py
from dao.tools import *


class AuthenticationLogic:
    def __init__(self):
        pass

    def login(self, input_id, input_password, type):
        """
        登录验证
        :param input_id: 用户id
        :param input_password: 用户密码
        :param type: 用户类型
        :return: 用户数据
        """
        datas = tools().load_data(type)
        for data in datas:
            if data["id"] == input_id and data["password"] == input_password:
                return data