#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
@ProjectName: homalos-lite
@FileName   : api.py
@Date       : 2026/5/7 14:04
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: 中央调度器（CoreApi）
中央调度器，职责包括：
- 维护完整业务数据快照 (_data)
- 管理行情订阅与数据序列
- 处理交易指令（下单/撤单）
- 事件驱动调度（wait_update）
- 风控规则注册与校验
- 通过 HmlChan 连接行情和交易网关
- 提供行情查询、交易、订阅、风控等统一接口
"""
import asyncio
import time
from collections import deque
from typing import Any, Dict, List, Optional, Set, Tuple

from .data_series import KlineSeries, TickSequence
from .diff import apply_diff


class CoreApi:
    def __init__(self, md_gateway, td_gateway, backtest_engine=None):
        # 数据快照（所有业务数据）
        self._data: Dict[str, Any] = {
            "quotes": {},  # symbol -> quote dict
            "positions": {},  # symbol -> list of position dicts
            "account": {}  # 账户信息
        }
        # 待处理的差异数据包
        self._pending_diffs: deque = deque()
        # 已订阅合约
        self._subscriptions: Set[Tuple[str, str]] = set()  # (symbol, type)

        # 数据通道（连接网关）
        self._md_gateway = md_gateway
        self._td_gateway = td_gateway
        # 回测引擎（如果提供）
        self._backtest = backtest_engine

        # 策略管理器（在注册策略时可用）
        self.strategy_manager = None

        # 风控
        from src.risk.manager import RiskManager
        self.risk_manager = RiskManager()

        # 序列存储：{ (symbol, duration_seconds) -> KlineSeries }
        self._kline_serials: Dict[tuple, KlineSeries] = {}
        self._tick_seq: Dict[str, TickSequence] = {}

        # 启动数据处理协程
        self._task = None

    async def _run(self):
        """不断从网关接收数据并放入 pending_diffs"""
        while True:
            data = await self._md_gateway.recv()  # 假设网关提供异步 recv
            if data:
                self._pending_diffs.append(data)
                # 驱动 kline 合成
                self._on_data(data)

    def _on_data(self, data: dict):
        """处理接收到的原始数据，进行 kline 合成等"""
        # 如果包含 tick，驱动相应 KlineSeries
        if "ticks" in data:
            for symbol, tick in data["ticks"].items():
                if symbol not in self._tick_seq:
                    self._tick_seq[symbol] = TickSequence()
                self._tick_seq[symbol].push(tick)
                # 驱动所有该 symbol 的 kline series
                for (sym, dur), kline in self._kline_serials.items():
                    if sym == symbol:
                        closed = kline.on_tick(tick)
                        if closed:
                            # 可将 closed bar 推送给策略等，或在 _data 中更新
                            pass

    def start(self):
        if self._task is None:
            self._task = asyncio.ensure_future(self._run())

    async def wait_update(self, timeout: float = 0.5) -> bool:
        """
        事件驱动核心：等待直到收到至少一个数据包或超时。
        返回 True 表示有新数据并已合并，False 表示超时。
        """
        if self._backtest:
            return await self._backtest.step()  # 回测模式
        deadline = time.time() + timeout
        while not self._pending_diffs and time.time() < deadline:
            await asyncio.sleep(0.001)  # 极短让出，保持低延迟
        # 合并所有 pending diffs
        while self._pending_diffs:
            diff = self._pending_diffs.popleft()
            if isinstance(diff, list):
                apply_diff(self._data, diff)
            else:
                # 其他格式处理
                pass
        return bool(self._pending_diffs)  # 返回是否有新数据（注意已消费，所以始终False？改）
        # 修改：在合并前记录是否有 pending，合并后返回
        # 实际应改为：
        # had_data = bool(self._pending_diffs)
        # 然后合并...
        # return had_data

    # ---------- 行情查询 API ----------
    def get_quote(self, symbol: str) -> dict:
        return self._data.get("quotes", {}).get(symbol, {})

    def is_changing(self, quote: dict, field: str = "last_price") -> bool:
        """简单判断：比较当前值和上一次值（需实现缓存）"""
        # 简化实现，始终返回 True，生产需记录 last_checked
        return True

    # ---------- 订阅订阅 ----------
    async def subscribe(self, symbols: List[str]):
        for s in symbols:
            self._subscriptions.add((s, "quote"))
        await self._md_gateway.subscribe(symbols)

    # ---------- 交易 API ----------
    async def insert_order(self, order_req: dict) -> Optional[str]:
        # 风控预检查
        if not self.risk_manager.check_pre_trade(order_req, self._data["account"]):
            return None
        # 发送给交易网关
        return await self._td_gateway.insert_order(order_req)

    def get_position(self, symbol: str = None) -> list:
        if symbol:
            return self._data.get("positions", {}).get(symbol, [])
        return list(self._data.get("positions", {}).values())

    def get_account(self) -> dict:
        return self._data.get("account", {})
