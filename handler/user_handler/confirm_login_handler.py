# -*- coding: UTF-8 -*-
"""
    @file   login_handler
    @author zh1995
    @date   17-4-1
    @brief    
"""

import tornado.web
import logging
import json
import traceback
from model.lemo.login import Login
from model.tool.json_encode import json_encode

class ConfirmLoginHandler(tornado.web.RequestHandler):

    """
    
    """
    def initialize(self):
        self.logger = logging.getLogger(name='handler')
        self.add_header("Access-Control-Allow-Origin", "*")

    def get(self):
        """
        通过账号、密码登录
        @:param string account
        @:param string passward
        """
        self.logger.info("ConfirmLoginHandler_start")

        try:
            # argument = json.loads(self.request.body)
            # self.logger.info("arguments=%s", argument)
            # username = argument['username']
            # password = argument['password']
            username = self.get_argument("username")
            password = self.get_argument("password")
        except Exception, e:
            self.logger.error("e = %s", e)
            self.logger.error(traceback.format_exc())
            self.logger.error("ConfirmLoginHandler_error_getArgument")
            self.write(json_encode('fail', 'get argument failed'))
            return

        try:
            login_info = Login().confirm_user_login(username=username, password=password)
        except Exception, e:
            self.logger.error("e = %s", e)
            self.logger.error(traceback.format_exc())
            self.logger.error("ConfirmLoginHandler_error_getLoginInfo")
            self.write(json_encode('fail', 'get argument failed'))
            return

        login_info = json.dumps(login_info).encode('utf8')

        self.logger.info("ConfirmLoginHandler_over")
        self.write(login_info)