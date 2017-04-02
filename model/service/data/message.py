# -*- coding: UTF-8 -*-
# @file   message
# @author zh1995
# @date   17-4-2
# @brief

from model.dao.sql_operation import SQL


class Message(object):
    """
    文章类
    """

    def __init__(self):
        """
        初始化类
        """
        pass

    def get_message_list(self, offset = 0, limit = 10):
        """
        获取文章列表
        :param offset: 
        :param limit: 
        :return: 
        """
        sql_sentence = "SELECT message_id, message_title, cover_pic FROM tblMessage ORDER BY create_time DESC LIMIT %s, %s"
        param_list = (offset, limit)
        return SQL().fetch_all(sql_sentence, param_list)

    def get_total_message_count(self):
        """
        
        :return: 
        """
        sql_sentence = "SELECT COUNT(1) FROM tblMessage"
        res = SQL().fetch_all(sql_sentence)
        return res[0]

    def get_message_content(self, message_id):
        """
        
        :param message_id: 
        :return: 
        """
        sql_sentence = "SELECT message_title, cover_pic, author_name, author_img, message_content, look_num, good_num, create_time FROM tblMessage WHERE message_id=%s"
        param_list = (message_id, )
        return SQL().fetch_one(sql_sentence, param_list)

    def get_hotspot_list(self):
        """
        
        :return: 
        """
        sql_sentence = "SELECT message_id, message_title, cover_pic FROM tblMessage ORDER BY good_num DESC LIMIT 0, 4"
        return SQL().fetch_all(sql_sentence)