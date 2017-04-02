# -*- coding: UTF-8 -*-
# @file   hotspot
# @author zh1995
# @date   17-4-2
# @brief

from base_page import BasePage
from model.service.data.message import Message


class Hotspot(BasePage):
    """
    热点列表类
    """

    def _execute(self, req):
        """
        执行函数
        :param req: 
        :return: 
        """
        hotspot_list = Message().get_hotspot_list()
        return {
            "data": self._format_hotspot_list(hotspot_list),
        }

    def _format_hotspot_list(self, hotspot_list):
        """

        :param hotspot_list: 
        :return: 
        """
        if hotspot_list is None:
            return hotspot_list
        new_hotspot_list = []
        for message in hotspot_list:
            new_hotspot_list.append(
                {
                    "message_id": message[0],
                    "message_title": message[1],
                    "cover_pic": message[2],
                }
            )
        return new_hotspot_list