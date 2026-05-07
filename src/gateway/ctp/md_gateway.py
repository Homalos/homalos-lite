#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
@ProjectName: homalos-lite
@FileName   : md_gateway.py
@Date       : 2026/5/7 14:16
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: CTP行情网关
"""

from typing import List, Any

from src.core.channel import HmlChan
from src.gateway.base import BaseMdGateway
from src.gateway.market_enums import MarketDataType
from src.utils.utility import prepare_address


class CtpMdGateway(BaseMdGateway):
    """CTP行情网关（基于上期技术 CTP API 的 Python 封装）"""

    def __init__(self, recv_chan: HmlChan, front_addr: str, broker_id: str):
        super().__init__(recv_chan)
        self._front_addr = front_addr
        self._broker_id = broker_id
        self._api = None  # CThostFtdcMdApi 实例

    async def recv(self):
        pass

    async def connect(self, setting: dict[str, Any]):
        """连接CTP行情前置"""
        # CTP行情API连接逻辑
        md_address = setting.get("md_address", "")  # 行情服务器地址
        broker_id = setting.get("broker_id", "")  # 经纪商代码
        user_id = setting.get("user_id", "")  # 用户名
        password = setting.get("password", "")  # 密码

        # 参数验证
        if not all([md_address, broker_id, user_id, password]):
            self.logger.error("缺少必需的连接参数")

        md_address = prepare_address(md_address)

        try:
            # 创建API实例
            if not self.md_api:
                self.md_api = CtpMdApi(self)
            # 连接行情服务器
            self.md_api.connect(md_address, broker_id, user_id, password)
        except Exception as e:
            self.logger.exception(f"连接失败: {e}")
            if self.md_api:
                self.md_api.close()

    async def subscribe(self, symbols: List[str], data_type: MarketDataType):
        for symbol in symbols:
            self._requests.add((symbol, data_type))

    async def _on_market_data(self, data: dict):
        """行情数据回调：收到后立即放入 recv_chan"""
        await self._recv_chan.put(data)

    async def unsubscribe(self, symbols: List[str]):
        pass

    async def close(self):
        pass
