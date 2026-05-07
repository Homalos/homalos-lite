#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
@ProjectName: homalos-lite
@FileName   : engine.py
@Date       : 2026/5/7 14:34
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: 基于历史数据的模拟行情和交易
实际集成时，在 CoreApi.__init__ 中若提供 backtest，
则在 wait_update 中调用 backtest.step() 来推进时间，并更新 api._data。
"""
from collections import deque
from typing import List, Dict

from src.core.data_series import KlineSeries, TickSequence


class TickGenerator:
    """从历史 tick 数据生成 ticks"""
    def __init__(self, tick_data: List[dict]):
        self._ticks = deque(tick_data)
        self.current = None

    def next(self) -> dict:
        if self._ticks:
            self.current = self._ticks.popleft()
            return self.current
        return None

class BacktestEngine:
    def __init__(self, start_dt: float, end_dt: float):
        self._start = start_dt
        self._end = end_dt
        self._current_dt = start_dt
        self._tick_generators: Dict[str, TickGenerator] = {}
        self._tick_seq: Dict[str, TickSequence] = {}
        self._kline_serials: Dict[tuple, KlineSeries] = {}

    def load_tick_data(self, symbol: str, tick_data: List[dict]):
        self._tick_generators[symbol] = TickGenerator(tick_data)
        self._tick_seq[symbol] = TickSequence()

    async def step(self) -> bool:
        """推进一个时间步（最早的下一个 tick），更新 _data"""
        # 找出所有 generator 中下一个 tick 的最小时间
        next_tick = None
        next_symbol = None
        for sym, gen in self._tick_generators.items():
            t = gen.current or gen.next()
            if t and (next_tick is None or t["datetime"] < next_tick["datetime"]):
                next_tick = t
                next_symbol = sym
        if next_tick is None:
            return False  # 数据耗尽

        self._current_dt = next_tick["datetime"]
        # 更新到 api._data
        # 此处需要 CoreApi 的引用，通常构建回测时传入
        # 简化：直接修改 api._data["quotes"][symbol]
        return True

    async def generate_data_packet(self, api) -> dict:
        """返回一个拟合成的 diff 数据包，供 api 消费"""
        # 这个 step 已内置在 wait_update 的回测分支中
        ...
