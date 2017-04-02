# -*- coding: UTF-8 -*-
# @file   user
# @author zh1995
# @date   17-4-1
# @brief

from model.dao.sql_operation import SQL

class User(object):
    """
    登录类
    """
    def __init__(self):
        """
        初始化类
        """
        pass

    def select_uid_by_name_and_pwd(self, username, password):
        """
        
        :param username: 
        :param password: 
        :return: 
        """
        sql_sectence = "SELECT uid FROM tblUser WHERE uname=%s and password=%s"
        param_list = (username, password)
        return SQL().fetch_one(sql_sectence, param_list)
