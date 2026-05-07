#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
@ProjectName: homalos-lite
@FileName   : diff.py
@Date       : 2026/5/7 14:51
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: DIFF 协议增量合并
"""
from typing import Any, Dict, List


def apply_diff(data: Dict[str, Any], diffs: List[Dict[str, Any]]) -> None:
    """
    将 diff 列表合并到 data 字典中。
    diff 对象格式: {"path": ["quotes", "SHFE.cu2305", "last_price"], "value": 68801}
    """
    for diff in diffs:
        path = diff.get("path", [])
        value = diff.get("value")
        if not path:
            continue
        # 按路径导航到父对象
        obj = data
        for key in path[:-1]:
            if key not in obj:
                obj[key] = {}
            obj = obj[key]
        # 设置最终值
        if value is None:
            # 删除键
            if isinstance(obj, dict) and path[-1] in obj:
                del obj[path[-1]]
        else:
            obj[path[-1]] = value
