#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
@ProjectName: homalos-lite
@FileName   : td_gateway.py
@Date       : 2026/5/7 14:24
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: description
"""
from src.gateway.base import BaseTdGateway


class CtpTdGateway(BaseTdGateway):
    """CTP交易网关"""

    async def insert_order(self, order: dict) -> str:
        packet = {"aid": "insert_order", "data": order}
        await self._send_chan.put(packet)
        return order.get("order_id", "")

    async def cancel_order(self, order_id: str):
        pass

    async def get_account(self) -> dict:
        pass

    async def get_position(self, symbol: str = None) -> list:
        pass
