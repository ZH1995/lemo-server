# -*- coding: UTF-8 -*-
# @file   hotspot
# @author zh1995
# @date   17-4-2
# @brief
import redis
from base_page import BasePage
from model.service.data.user_message_action_map import UserMessageActionMap
from model.service.data.message import Message


class Hotspot(BasePage):
    """
    热点列表类
    """
    def _check_param(self):
        """
        参数校验
        :return: 
        """
        if self._get_param("uid") is None:
            raise Exception("uid is none")
        if self._get_param("current_page") is None:
            raise Exception("current_page is none")
        if self._get_param("page_size") is None:
            raise Exception("page_size is none")

    def _execute(self, req):
        """
        执行函数
        :param req: 
        :return: 
        """
        # 转义参数
        uid = int(self._get_param("uid"))
        current_page = int(self._get_param("current_page"))
        page_size = int(self._get_param("page_size"))

        # 计算偏移
        offset = current_page * page_size

        ds_action_map = UserMessageActionMap()
        record_count = ds_action_map.get_online_record_count_by_uid(uid)
        # 没有交互查数据库
        if record_count == 0:
            hotspot_list = self._get_normal_recommend_message_list(uid, offset, page_size)
        # 有交互进行推荐策略
        else:
            hotspot_list = self._get_user_recommend_message_list(uid, offset, page_size)
        return {
            "data": {
                "list": self._format_message_list(hotspot_list)
            }
        }

    def _get_user_recommend_message_list(self, uid, offset, page_size):
        """
        
        :param uid: 
        :param offset: 
        :param page_size: 
        :return: 
        """
        pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0)
        r = redis.StrictRedis(connection_pool=pool)
        user_key_name = "recommend_uid_" + str(uid)
        if r.exists(user_key_name) is False:
            return False
        mid_list = r.lrange(user_key_name, 0, r.llen(user_key_name))
        if len(mid_list) is 0:
            return False
        # 获取与当前用户相关的其他用户
        other_uid_list = []
        for mid in mid_list:
            mid_key_name = "recommend_mid_" + str(mid)
            if r.exists(mid_key_name) is False:
                continue
            mid_uid_list = r.lrange(mid_key_name, 0, r.llen(mid_key_name))
            for other_uid in mid_uid_list:
                if other_uid == uid or other_uid in other_uid_list:
                    continue
                other_uid_list.append(other_uid)

        # 获取前K个用户
        ds_action_map = UserMessageActionMap()
        user_weight_dict = {}
        for other_uid in other_uid_list:
            weight = 0
            for mid in mid_list:
                if ds_action_map.has_online_relation(mid, uid) is False:
                    weight += 1
            user_weight_dict[other_uid] = weight
        user_weight_dict = sorted(user_weight_dict.iteritems(), key=lambda val: val[1], reverse=False)
        k = 3
        if len(other_uid_list) <= k:
            k = len(other_uid_list)
        other_uid_list = []
        idx = 0
        for uid in user_weight_dict:
            if idx >= k:
                break
            other_uid_list.append(uid)
            idx += 1
        # 取前K个用户的文章ID
        other_mid_list = []
        for other_uid in other_uid_list:
            uid_key_name = "recommend_uid_" + str(other_uid)
            if r.exists(uid_key_name) is False:
                continue
            uid_mid_list = r.lrange(uid_key_name, 0, r.llen(uid_key_name))
            for other_mid in uid_mid_list:
                if other_mid in other_mid_list or other_mid in mid_list:
                    continue
                other_mid_list.append(other_mid)
        ds_message = Message()
        message_list = ds_message.get_message_list_by_message_id_list(other_mid_list)
        return message_list

    def _get_normal_recommend_message_list(self, uid, offset, page_size):
        """
        
        :param uid: 
        :param offset: 
        :param page_size: 
        :return: 
        """
        pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0)
        r = redis.StrictRedis(connection_pool=pool)
        key_name = "recommend_mid_list"
        if r.exists(key_name) is False:
            return False
        mid_list = r.lrange(key_name, offset, page_size)
        if len(mid_list) is 0:
            return False
        for mid in mid_list:
            mid_list[mid] = int(mid)
        ds_message = Message()
        message_list = ds_message.get_message_list_by_message_id_list(mid_list)
        return message_list

    def _format_message_list(self, message_list):
        """
        格式化文章列表
        :param message_list:  
        :return: 
        """
        if message_list is None:
            return message_list
        new_message_list = []
        for message in message_list:
            new_message_list.append(
                {
                    "messageId": message[0],
                    "messageTitle": message[1],
                    "coverPic": message[2],
                }
            )
        return new_message_list