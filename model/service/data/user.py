# -*- coding: UTF-8 -*-
# @file   user
# @author zh1995
# @date   17-4-1
# @brief

import datetime
import time
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

    def get_uid_by_name_and_pwd(self, username, password):
        """
        根据用户名、密码获取用户ID
        :param username: 
        :param password: 
        :return: 
        """
        sql_sentence = "SELECT uid FROM tblUser WHERE uname=%s and password=%s"
        param_list = (username, password)
        return SQL().fetch_one(sql_sentence, param_list)

    def add_new_user(self, username, password, headimg = ""):
        """
        
        :param username: 
        :param password: 
        :param headimg: 
        :return: 
        """
        sql_sentence = "INSERT INTO tblUser (`uname`, `password`, `head_img`, `create_time`) VALUES (%s, %s, %s, %s)"
        create_time = int(time.mktime(datetime.datetime.now().timetuple()))
        param_list = (username, password, headimg, create_time)
        return SQL().execute_one(sql_sentence, param_list)