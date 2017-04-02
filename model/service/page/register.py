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
        if self._get_param("password") is None:
            raise Exception("Password is invalid")

    def _execute(self, req):
        """
        执行函数
        :param req: 
        :return: 
        """
        username = str(self._get_param("username"))
        password = str(self._get_param("password"))
        if self.__is_exist(username, password) is True:
            return {
                "errno": -1,
                "errmsg": "account has exist",
            }

        create_user_res = User().add_new_user(username, password)
        if create_user_res is None:
            return {
                "errno": -1,
                "errmsg": "create account fail",
            }

        uid = User().get_uid_by_name_and_pwd(username, password)
        return {
            "data": {
                "uid": uid[0]
            }
        }

    def __is_exist(self, username, password):
        """
        
        :param username: 
        :param password: 
        :return: 
        """
        uid = User().get_uid_by_name_and_pwd(username, password)
        if uid[0] is None:
            return False
        return True