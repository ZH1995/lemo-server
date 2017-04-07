# -*- coding: UTF-8 -*-
# @file   register
# @author zh1995
# @date   17-4-1
# @brief

from base_page import BasePage
from model.service.data.user import User


class Register(BasePage):
    """
    注册类
    """

    def _check_param(self):
        """
        参数校验
        :return: 
        """
        if self._get_param("username") is None:
            raise Exception("User name is invalid")
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
        username = str(self._get_param("username"))
        phone_number = str(self._get_param("phone_number"))
        password = str(self._get_param("password"))
        if self.__is_exist(phone_number, password) is True:
            return {
                "errno": -1,
                "errmsg": "account has exist",
            }

        create_user_res = User().add_new_user(username, phone_number, password)
        if create_user_res is None:
            return {
                "errno": -1,
                "errmsg": "create account fail",
            }

        uid = User().get_uid_by_phone_and_pwd(phone_number, password)
        return {
            "data": {
                "uid": uid[0]
            }
        }

    def __is_exist(self, phone_number, password):
        """
        
        :param phone_number: 
        :param password: 
        :return: 
        """
        uid = User().get_uid_by_phone_and_pwd(phone_number, password)
        if uid is None:
            return False
        return True
