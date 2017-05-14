# -*- coding: UTF-8 -*-
# @file   hotspot
# @author zh1995
# @date   17-4-2
# @brief

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
            hotspot_list = self._get_db_list(uid, offset, page_size)
        # 有交互进行推荐策略
        else:
            hotspot_list = self._get_recommend_list(uid, offset, page_size)
        return {
            "data": {
                "list": self._format_message_list(hotspot_list)
            }
        }


    def _get_db_list(self, uid, offset, page_size):
        """
        
        :param uid: 
        :param offset: 
        :param page_size: 
        :return: 
        """
        ds_message = Message()
        message_list = ds_message.get_message_list_by_look_num(offset, page_size)
        return message_list

    def _get_mid_list_by_uid(self, uid):
        """
        
        :param uid: 
        :return: 
        """
        ds_action_map = UserMessageActionMap()
        msg_map_list = ds_action_map.get_msg_map_list_by_uid(uid)
        message_id_list = []
        for map in msg_map_list:
            message_id_list.append(map["message_id"])
        return message_id_list

    def _get_uid_list_by_mid_list(self, message_id_list):
        """
        
        :param message_id_list: 
        :return: 
        """
        ds_action_map = UserMessageActionMap()
        user_map_list = ds_action_map.get_user_map_list(message_id_list)
        uid_list = []
        for map in user_map_list:
            uid_list.append(map["uid"])
        return uid_list

    def _get_uid_mid_dict(self, other_uid_list):
        """
        
        :param other_uid_list: 
        :return: 
        """
        uid_mid_dict = {}
        for uid in other_uid_list:
            uid_mid_dict[uid] = self._get_mid_list_by_uid(uid)
        return uid_mid_dict

    def _get_k_uid_list(self, cur_msg_id_list, other_uid_list, other_uid_mid_dict, k):
        """
        
        :param cur_msg_id_list: 
        :param other_uid_list: 
        :param other_uid_mid_dict: 
        :return: 
        """
        uid_map_dict = {}
        for uid in other_uid_list:
            # 计算集合差集
            tmp = [val for val in cur_msg_id_list if val in other_uid_mid_dict[uid]]
            uid_map_dict[uid] = len(tmp)

        uid_map_dict = sorted(uid_map_dict, key=lambda asd: asd[1], reverse=True)
        k_uid_list = []
        idx = 0
        for uid in uid_map_dict:
            if idx >= k:
                break
            k_uid_list.append(uid)
            idx += 1
        return k_uid_list

    def _get_mid_list_by_k_user(self, other_uid_mid_dict, k_uid_list, offset, page_size):
        """
        
        :param other_uid_mid_dict: 
        :param k_uid_list: 
        :param offset: 
        :param page_size: 
        :return: 
        """
        mid_list = []
        for uid in k_uid_list:
            mid_list = list(set(mid_list).union(set(other_uid_mid_dict[uid])))
        return mid_list[offset:page_size]

    def _get_recommend_list(self, uid, offset, page_size):
        """
        
        :param uid: 
        :param offset: 
        :param page_size: 
        :return: 
        """
        # 获取当前用户有过交互的文章
        cur_msg_id_list = self._get_mid_list_by_uid(uid)
        # 取有交集的其他用户集合
        other_uid_list = self._get_uid_list_by_mid_list(cur_msg_id_list)
        # 获取其他用户的文章ID集合
        other_uid_mid_dict = self._get_uid_mid_dict(other_uid_list)
        # 取前k个用户
        k = 3
        k_uid_list = self._get_k_uid_list(cur_msg_id_list, other_uid_list, other_uid_mid_dict, k)
        # 获取推送文章列表
        mid_list = self._get_mid_list_by_k_user(other_uid_mid_dict, k_uid_list, offset, page_size)
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