#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
@ProjectName: homalos-lite
@FileName   : manager.py
@Date       : 2026/5/7 14:32
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: 可插拔风控管理器
"""
from typing import List

from src.risk.risk_enums import RiskLevel
from src.risk.rules import RiskRule


class RiskManager:
    def __init__(self):
        self._rules: List[RiskRule] = []

    def add_rule(self, rule: RiskRule):
        self._rules.append(rule)

    def remove_rule(self, name: str):
        self._rules = [r for r in self._rules if r.name != name]

    def check_pre_trade(self, order_req: dict, account: dict) -> bool:
        for rule in self._rules:
            if rule.level == RiskLevel.PRE_TRADE:
                if not rule.check(order_req, account):
                    if rule.action == "reject":
                        return False
        return True
