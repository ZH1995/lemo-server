# -*- coding: UTF-8 -*-
"""
    @file   json_encode
    @author zh1995
    @date   17-4-1
    @brief    
"""

import json

def json_encode(result, fail_reason):
    """
    封装返回结果信息
    :param result: 业务结果 
    :param fail_reason: 失败原因（success时为空）
    :return: 
    """
    return json.dumps(
        {
            'result': result,
            'fail_reason': fail_reason,
        }
    ).encode('utf8')