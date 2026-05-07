#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
@ProjectName: homalos-lite
@FileName   : manager.py
@Date       : 2026/5/7 14:33
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: 多策略管理器
"""
from typing import Dict
from .base import BaseStrategy

class StrategyManager:
    def __init__(self, api):
        self.api = api
        self._strategies: Dict[str, BaseStrategy] = {}
        api.strategy_manager = self

    def register(self, strategy: BaseStrategy):
        self._strategies[strategy.name] = strategy

    async def start_all(self):
        for s in self._strategies.values():
            await s.start()

    async def stop_all(self):
        for s in self._strategies.values():
            await s.stop()

    async def stop_one(self, name: str):
        if name in self._strategies:
            await self._strategies[name].stop()

    def list_strategies(self):
        return {name: {"running": s._running} for name, s in self._strategies.items()}
