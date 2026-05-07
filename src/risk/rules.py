#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
@ProjectName: homalos-lite
@FileName   : rules.py
@Date       : 2026/5/7 14:31
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: description
"""
from typing import Callable

from src.risk.risk_enums import RiskLevel


class RiskRule:
    def __init__(self, name: str, level: RiskLevel, check: Callable, action: str = "reject"):
        self.name = name
        self.level = level
        self.check = check  # 检查函数: (order_req, account) -> bool
        self.action = action  # "reject" / "warn"
