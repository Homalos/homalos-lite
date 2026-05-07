#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
@ProjectName: homalos-lite
@FileName   : server.py
@Date       : 2026/5/7 14:36
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: FastAPI 主程序
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from .ws_manager import ConnectionManager
from .routes import setup_routes
import uvicorn

def create_app(api) -> FastAPI:
    app = FastAPI(title="Quant Futures Trading System")
    manager = ConnectionManager()

    @app.websocket("/ws/rtn_data")
    async def websocket_endpoint(ws: WebSocket):
        await manager.connect(ws)
        # 发送初始快照
        await ws.send_json({"aid": "rtn_data", "data": [api._data]})
        try:
            while True:
                # 接收客户端命令（忽略）
                await ws.receive_text()
                # 后续可以实现从 api 推送增量数据
        except WebSocketDisconnect:
            manager.disconnect(ws)

    setup_routes(app, api)
    return app
