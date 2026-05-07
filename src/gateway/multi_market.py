#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
@ProjectName: homalos-lite
@FileName   : multi_market.py
@Date       : 2026/5/7 14:21
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: description
"""
from typing import Dict, List

from src.core.channel import HmlChan
from src.gateway.base import BaseMdGateway
from src.gateway.market_enums import MarketDataType


class MultiMarketGateway(BaseMdGateway):
    """
    多市场源代理网关：统一管理多个子网关
    支持CTP + 其他期货市场源的同时接入
    """

    def __init__(self, recv_chan: HmlChan):
        super().__init__(recv_chan)
        self._gateways: Dict[str, BaseMdGateway] = {}

    def add_gateway(self, name: str, gateway: BaseMdGateway):
        self._gateways[name] = gateway

    async def subscribe(self, symbols: List[str], data_type: MarketDataType):
        for gw in self._gateways.values():
            await gw.subscribe(symbols, data_type)

    async def unsubscribe(self, symbols: List[str]):
        pass

    async def connect(self):
        pass

    async def close(self):
        pass
