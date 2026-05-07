#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
@ProjectName: homalos-lite
@FileName   : market_enums.py
@Date       : 2026/5/7 14:20
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: description
"""
from enum import Enum


class MarketDataType(Enum):
    TICK = "tick"
    KLINE = "kline"
    QUOTE = "quote"
    DEPTH = "depth"
