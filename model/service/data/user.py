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

    def get_uid_by_phone_and_pwd(self, phone_number, password):
        """
        根据电话号、密码获取用户ID
        :param phone_number: 
        :param password: 
        :return: 
        """
        sql_sentence = "SELECT uid FROM tblUser WHERE phone_number=%s and password=%s"
        param_list = (phone_number, password)
        return SQL().fetch_one(sql_sentence, param_list)


    def add_new_user(self, username, phone_number, password, headimg=""):
        """
        
        :param username:
        :param phone_number:
        :param password: 
        :param headimg: 
        :return: 
        """
        sql_sentence = "INSERT INTO tblUser (`uname`, `phone_number`, `password`, `head_img`, `create_time`) VALUES (%s, %s, %s, %s, %s)"
        create_time = int(time.mktime(datetime.datetime.now().timetuple()))
        param_list = (username, phone_number, password, headimg, create_time)
        return SQL().execute_one(sql_sentence, param_list)