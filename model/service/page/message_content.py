# -*- coding: UTF-8 -*-
# @file   message_content
# @author zh1995
# @date   17-4-2
# @brief


from base_page import BasePage
from model.service.data.message import Message


class MessageContent(BasePage):
    """
    文章内容类
    """

    def _check_param(self):
        """
        参数校验
        :return: 
        """
        if self._get_param("message_id") is None:
            raise Exception("message page is invalid")

    def _execute(self, req):
        """
        执行函数
        :param req: 
        :return: 
        """
        message_id = int(self._get_param("message_id"))
        message_content = Message().get_message_content(message_id)
        return {
            "data": self._format_message_content(message_content),
        }

    def _format_message_content(self, message_content):
        """

        :param message_content: 
        :return: 
        """
        if message_content is None:
            return message_content
        return {
            "message_title": message_content[0],
            "cover_pic": message_content[1],
            "author_name": message_content[2],
            "author_img": message_content[3],
            "message_content": message_content[4],
            "look_num": message_content[5],
            "good_num": message_content[6],
            "create_time": message_content[7],
        }