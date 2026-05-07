#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
@ProjectName: homalos-lite
@FileName   : entity.py
@Date       : 2026/5/7 14:50
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: 数据快照的实体定义
这里采用类似 TqSdk 的“扁平化 Entity 树”思想，用嵌套字典模拟。
为简化，直接使用 dict 存储，未定义复杂类。实际可用 dataclass 或 pydantic 增强。
"""
# 预留，本实现中直接以内置 dict 表示 quote、position 等
# 例如 quote 结构示例：
# {
#   "symbol": "SHFE.cu2305",
#   "datetime": 1680000000,
#   "last_price": 68800.0,
#   "volume": 12345,
#   "open_interest": 67890,
#   ...
# }