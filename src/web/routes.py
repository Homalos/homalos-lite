#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
@ProjectName: homalos-lite
@FileName   : routes.py
@Date       : 2026/5/7 15:03
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: REST API 实现
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class OrderRequest(BaseModel):
    symbol: str
    direction: str  # BUY/SELL
    offset: str     # OPEN/CLOSE
    price: float = 0
    volume: int

def setup_routes(app, api):
    @router.get("/api/account")
    async def get_account():
        return api.get_account()

    @router.get("/api/positions")
    async def get_positions(symbol: Optional[str] = None):
        return api.get_position(symbol)

    @router.post("/api/order")
    async def place_order(order: OrderRequest):
        oid = await api.insert_order(order.dict())
        if oid:
            return {"status": "ok", "order_id": oid}
        raise HTTPException(status_code=400, detail="Order rejected by risk check")

    @router.get("/api/strategies")
    async def list_strategies():
        if api.strategy_manager:
            return api.strategy_manager.list_strategies()
        return {}

    @router.post("/api/strategy/{name}/start")
    async def start_strategy(name: str):
        if api.strategy_manager:
            await api.strategy_manager.start_one(name)
            return {"status": "started"}
        raise HTTPException(status_code=404)

    app.include_router(router)
