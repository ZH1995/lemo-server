# -*- coding: UTF-8 -*-
"""
    @file   user
    @author zh1995
    @date   17-4-1
    @brief    
"""


def select_uid_by_name_and_pwd(username, password):
    """
    
    :param username: 
    :param password: 
    :return: 
    """
    return """
            SELECT uid FROM tblUser
            WHERE uname = '%s' and password = '%s'
        """ % (username, password)
