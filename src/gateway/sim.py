#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
@ProjectName: homalos-lite
@FileName   : sim.py
@Date       : 2026/5/7 14:25
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: 模拟交易网关（用于回测）
"""
from .base import BaseTdGateway

class SimTdGateway(BaseTdGateway):
    """简单模拟成交：下单立刻全部成交"""
    def __init__(self):
        self._orders = {}
        self._order_counter = 0

    async def insert_order(self, order_req: dict) -> str:
        self._order_counter += 1
        oid = f"sim_{self._order_counter}"
        order = {
            "order_id": oid,
            "symbol": order_req["symbol"],
            "direction": order_req["direction"],
            "offset": order_req["offset"],
            "price": order_req.get("price", 0),
            "volume": order_req["volume"],
            "status": "FILLED",
            "filled_volume": order_req["volume"],
            "filled_price": order_req.get("price", 0)  # 简化
        }
        self._orders[oid] = order
        # 模拟通知 CoreApi：需要一种机制将 order 状态推送回 api._data
        # 这里简化，实际应由网关通过 send_chan 发送 diff
        return oid

    async def cancel_order(self, order_id: str) -> bool:
        if order_id in self._orders and self._orders[order_id]["status"] == "PENDING":
            self._orders[order_id]["status"] = "CANCELLED"
            return True
        return False