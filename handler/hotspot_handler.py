# -*- coding: UTF-8 -*-
# @file   hotspot_handler
# @author zh1995
# @date   17-4-2
# @brief

import logging
import json
import tornado.web
from model.service.page.hotspot import Hotspot


class HotspotHandler(tornado.web.RequestHandler):
    """

    """

    def initialize(self):
        self.logger = logging.getLogger(name='handler')
        self.add_header("Access-Control-Allow-Origin", "*")
        self.handler_name = "HotspotContent"

    def post(self):
        """

        :return: 
        """
        self.logger.info("%s_start", self.handler_name)
        req = {}
        hotspot_list = Hotspot("Hotspot").execute(req)
        hotspot_list = json.dumps(hotspot_list).encode('utf8')

        self.logger.info("%s_over", self.handler_name)
        self.write(hotspot_list)
