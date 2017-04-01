# -*- coding: UTF-8 -*-
"""
    @file   login
    @author zh1995
    @date   17-4-1
    @brief    
"""

import logging
import traceback
from _mysql_exceptions import ProgrammingError
from model.sql import sql_statement
from model.tool import sql_operation, db_pool

class Login(object):
    """
    登录类
    """
    def __init__(self):
        self.logger = logging.getLogger(name="model")

    def confirm_user_login(self, username, password):
        """
        
        :param username: 
        :param password: 
        :return: 
        """
        self.logger.info("confirm_user_login_start, uname = %s", username)
        try:
            uid = self.get_uid_by_uname_and_pwd(username, password)
        except Exception, e:
            self.logger.error("e = %s", e)
            self.logger.error(traceback.format_exc())
            self.logger.error("get_uid_by_uname_and_pwd 失败")
            raise e
        return uid

    def get_uid_by_uname_and_pwd(self, username, password):
        """
        
        :param username: 
        :param password: 
        :return: 
        """
        self.logger.info("get_uid_by_uname_and_pwd_start, uname = %s", username)
        try:
            sql_sectence = sql_statement.user.select_uid_by_name_and_pwd(username, password)
            uid = sql_operation.SQL().fetch_one(sql_sectence)
            uid = uid[0]
        except Exception, e:
            self.logger.error("uname = %s 不存在", username)
            self.logger.error("e = %s", e)
            self.logger.error(traceback.format_exc())
            self.logger.error("select_uid_by_name_and_pwd 失败")
            raise e

        self.logger.info("get_uid_by_uname_and_pwd_over, uname = %s", username)
        return uid