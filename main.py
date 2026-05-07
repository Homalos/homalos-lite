#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
@ProjectName: homalos-lite
@FileName   : main.py
@Date       : 2026/5/7 14:02
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: 入口
"""
import asyncio

import uvicorn

from src.core.api import CoreApi
from src.gateway.sim import SimTdGateway
from src.strategy.base import BaseStrategy
from src.strategy.manager import StrategyManager
from src.web.server import create_app


class MyStrategy(BaseStrategy):
    async def on_init(self):
        await self.api.subscribe(self.symbols)
        print(f"Strategy {self.name} init, subscribed {self.symbols}")

    async def on_tick(self, tick: dict):
        # 此处实现真实策略逻辑
        print(f"{self.name} tick: {tick['datetime']} {tick['last_price']}")
        # 简单示例：每10个tick下一次单
        if int(tick['datetime']) % 10 == 0:
            await self.api.insert_order({
                "symbol": "SHFE.cu2305",
                "direction": "BUY",
                "offset": "OPEN",
                "price": tick['last_price'],
                "volume": 1
            })


async def main(HmlChan=None):
    # 创建网关（模拟买卖和行情）
    # 注意：gateway/sim.py 仅实现了交易网关，行情网关在示例中可以使用一个简单的 Mock
    # 这里我们假设已有一个 MockMdGateway 实现，或直接由 main 模拟数据注入
    # 为演示，我们直接在 api 中手动推送数据（示例简化）
    from src.core.channel import HmlChan
    class MockMd:
        def __init__(self):
            self._chan = HmlChan()

        async def subscribe(self, symbols): pass

        async def recv(self):
            # 从 channel 获取预先准备好的数据
            return await self._chan.get()

    md = MockMd()
    td = SimTdGateway()
    api = CoreApi(md_gateway=md, td_gateway=td)

    # 注册策略
    stm = StrategyManager(api)
    stm.register(MyStrategy(api, "test", ["SHFE.cu2305"]))
    await stm.start_all()

    # 启动网关协程
    asyncio.ensure_future(api._run())

    # 模拟行情数据注入
    async def mock_data():
        import time
        base_time = int(time.time())
        for i in range(100):
            await asyncio.sleep(0.1)
            tick = {
                "datetime": base_time + i,
                "symbol": "SHFE.cu2305",
                "last_price": 68800 + i,
                "volume": 5
            }
            # 直接推入 pending_diffs
            api._pending_diffs.append([{"path": ["quotes", "SHFE.cu2305"], "value": tick}])

    asyncio.ensure_future(mock_data())

    # 启动 Web 服务
    app = create_app(api)
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
