# -*- coding: UTF-8 -*-
# @file   message_list
# @author zh1995
# @date   17-4-2
# @brief

from base_page import BasePage
from model.service.data.message import Message



class MessageList(BasePage):
    """
    文章列表类
    """

    def _check_param(self):
        """
        参数校验
        :return: 
        """
        if self._get_param("page") is None:
            raise Exception("message page is invalid")

    def _execute(self, req):
        """
        执行函数
        :param req: 
        :return: 
        """
        page = int(self._get_param("page"))
        limit = int(self._get_param("limit"))
        offset = page * limit
        message_list = Message().get_message_list(offset, limit)
        return {
            "data": {
                "list": self._format_message_list(message_list),
                "total_count": Message().get_total_message_count(),
            }
        }

    def _format_message_list(self, message_list):
        """
        
        :param message_list: 
        :return: 
        """
        if message_list is None:
            return message_list
        new_message_list = []
        for message in message_list:
            new_message_list.append(
                {
                    "message_id": message[0],
                    "message_title": message[1],
                    "cover_pic": message[2],
                }
            )
        return new_message_list