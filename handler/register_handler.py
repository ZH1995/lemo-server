# -*- coding: UTF-8 -*-
# @file   register_handler
# @author zh1995
# @date   17-4-1
# @brief

import json
import logging
import tornado.web
from model.service.page.register import Register


class RegisterHandler(tornado.web.RequestHandler):
    """
    
    """

    def initialize(self):
        self.logger = logging.getLogger(name='handler')
        self.add_header("Access-Control-Allow-Origin", "*")
        self.handler_name = "RegisterHandler"

    def post(self):
        """
        
        :return: 
        """
        self.logger.info("%s_start", self.handler_name)
        try:
            argument = json.loads(self.request.body)
            self.logger.info("arguments=%s", argument)
        except Exception, e:
            self.logger.error("e = %s", e)
            return
        req = {
            "username": argument["username"],
            "phone_number": argument["phoneNumber"],
            "password": argument["password"],
        }
        uid_info = Register("Register").execute(req)
        uid_info = json.dumps(uid_info).encode('utf8')

        self.logger.info("%s_over", self.handler_name)
        self.write(uid_info)