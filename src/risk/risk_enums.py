#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
@ProjectName: homalos-lite
@FileName   : risk_enums.py
@Date       : 2026/5/7 14:26
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: description
"""
from enum import Enum


class RiskLevel(Enum):
    """风控层级"""
    PRE_TRADE = "pre_trade"     # 预交易风控
    EXECUTION = "execution"     # 执行中风控
    POST_TRADE = "post_trade"   # 事后风控