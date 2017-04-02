# -*- coding: UTF-8 -*-
# @file   login_handler
# @author zh1995
# @date   17-4-1
# @brief

import json
import logging
import traceback
import tornado.web
from model.service.page.login import Login

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

        # argument = json.loads(self.request.body)
        # self.logger.info("arguments=%s", argument)
        # username = argument['username']
        # password = argument['password']
        req = {
            "username": self.get_argument("username"),
            "password": self.get_argument("password"),
        }

        login_info = Login("Login").execute(req)
        login_info = json.dumps(login_info).encode('utf8')

        self.logger.info("ConfirmLoginHandler_over")
        self.write(login_info)