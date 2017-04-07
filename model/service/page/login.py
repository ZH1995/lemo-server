# -*- coding: UTF-8 -*-
# @file   login
# @author zh1995
# @date   17-4-1
# @brief

from base_page import BasePage
from model.service.data.user import User


class Login(BasePage):
    """
    登录类
    """

    def _check_param(self):
        """
        参数校验
        :return: 
        """
        if self._get_param("phone_number") is None:
            raise Exception("Phone number is invalid")
        if self._get_param("password") is None:
            raise Exception("Password is invalid")

    def _execute(self, req):
        """
        执行函数
        :param req: 
        :return: 
        """
        phone_number = str(self._get_param("phone_number"))
        password = str(self._get_param("password"))
        uid = User().get_uid_by_phone_and_pwd(phone_number, password)
        return {
            "data": {
                "uid": uid[0]
            }
        }