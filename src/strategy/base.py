#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
@ProjectName: homalos-lite
@FileName   : base.py
@Date       : 2026/5/7 14:33
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: 轻量策略基类
"""
from abc import ABC, abstractmethod
from typing import List, Optional
import asyncio

class BaseStrategy(ABC):
    """策略基类 —— 提供生命周期和钩子，但不强制继承"""
    def __init__(self, api, name: str, symbols: List[str]):
        self.api = api
        self.name = name
        self.symbols = symbols
        self._running = False
        self._task: Optional[asyncio.Task] = None

    @abstractmethod
    async def on_init(self):
        """初始化：订阅、指标准备等"""
        ...

    @abstractmethod
    async def on_tick(self, tick: dict):
        """tick 到来时的处理"""
        ...

    async def on_bar(self, bar):
        """K线闭合时触发（可选实现）"""
        pass

    async def on_order(self, order: dict):
        """订单状态变化回调（可选）"""
        pass

    async def start(self):
        self._running = True
        self._task = asyncio.ensure_future(self._run_loop())

    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
            self._task = None

    async def _run_loop(self):
        await self.on_init()
        while self._running:
            await self.api.wait_update()
            # 遍历监听的合约，如果 quote 有变化则触发 on_tick
            for symbol in self.symbols:
                quote = self.api.get_quote(symbol)
                if quote and self.api.is_changing(quote):
                    await self.on_tick(quote)
