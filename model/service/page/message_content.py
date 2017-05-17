# -*- coding: UTF-8 -*-
# @file   message_content
# @author zh1995
# @date   17-4-2
# @brief

import time
from base_page import BasePage
from model.service.data.message import Message
from model.service.data.comment import Comment
from model.service.data.user_message_action_map import UserMessageActionMap


class MessageContent(BasePage):
    """
    文章内容类
    """

    def _check_param(self):
        """
        参数校验
        :return: 
        """
        if self._get_param("uid") is None:
            raise Exception("uid is invalid")
        if self._get_param("message_id") is None:
            raise Exception("message page is invalid")

    def _execute(self, req):
        """
        执行函数
        :param req: 
        :return: 
        """
        # 转义参数
        uid = int(self._get_param("uid"))
        message_id = int(self._get_param("message_id"))




        # 获取文章内容
        ds_message = Message()
        message_content = ds_message.get_message_content_by_message_id(message_id)

        # 获取文章下评论总数
        ds_comment = Comment()
        comment_num = ds_comment.get_comment_num_by_message_id(message_id)

        # 浏览量+1
        add_look_num_res = ds_message.add_look_num_by_message_id(message_id)
        if add_look_num_res is None:
            self.logger.info("add look num fail")

        # 是否点过赞
        ds_user_message_action_map = UserMessageActionMap()
        good_action = 1
        has_good = ds_user_message_action_map.get_online_id_by_uid_and_message_id(uid, message_id, good_action)
        # 是否收藏过
        collect_action = 2
        has_collect = ds_user_message_action_map.get_online_id_by_uid_and_message_id(uid, message_id, collect_action)

        return {
            "data": self._format_message_content(message_content, comment_num[0], has_good, has_collect),
        }

    def _format_message_content(self, message_content, comment_num, has_good, has_collect):
        """

        :param message_content: 
        :param comment_num: 
        :param has_good: 
        :param has_collect: 
        :return: 
        """
        if message_content is None:
            return message_content
        return {
            "messageTitle": message_content[0],
            "coverPic": message_content[1],
            "authorName": message_content[2],
            "authorImg": message_content[3],
            "messageContent": message_content[4],
            "lookNum": message_content[5],
            "goodNum": message_content[6],
            "createTime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(message_content[7])),
            "commentNum": comment_num[0],
            "hasGood": True if has_good is not None else False,
            "hasCollect": True if has_collect is not None else False
        }
