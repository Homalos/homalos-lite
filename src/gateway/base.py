#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
@ProjectName: homalos-lite
@FileName   : base.py
@Date       : 2026/5/7 14:09
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: 抽象网关接口
BaseMdGateway / BaseTdGateway 抽象
"""
from abc import ABC, abstractmethod
from typing import List

class BaseMdGateway(ABC):
    @abstractmethod
    async def subscribe(self, symbols: List[str]) -> None:
        ...

    @abstractmethod
    async def recv(self):
        """异步取下一个数据包（行情数据）"""
        ...

class BaseTdGateway(ABC):
    @abstractmethod
    async def insert_order(self, order_req: dict) -> str:
        ...

    @abstractmethod
    async def cancel_order(self, order_id: str) -> bool:
        ...
