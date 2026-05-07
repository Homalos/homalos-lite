#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
@ProjectName: homalos-lite
@FileName   : data_series.py
@Date       : 2026/5/7 14:51
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: K线/Tick序列生成
"""
from collections import deque
from dataclasses import dataclass
from typing import Deque, List, Optional


@dataclass
class Bar:
    symbol: str
    datetime: float
    open: float
    high: float
    low: float
    close: float
    volume: int
    duration: float  # 周期秒数


class TickSequence:
    """简单的 Tick 序列缓存"""

    def __init__(self, max_len: int = 1024):
        self._ticks: Deque[dict] = deque(maxlen=max_len)

    def push(self, tick: dict) -> None:
        self._ticks.append(tick)

    def get_last(self) -> dict:
        return self._ticks[-1] if self._ticks else {}


class KlineSeries:
    """实时合成 K 线序列（由 tick 驱动）"""

    def __init__(self, symbol: str, duration: float, max_len: int = 500):
        self.symbol = symbol
        self.duration = duration
        self._bars: Deque[Bar] = deque(maxlen=max_len)
        self._cur_bar: Optional[Bar] = None

    def on_tick(self, tick: dict) -> Optional[Bar]:
        """收到 tick，更新当前 bar，若 bar 闭合则返回闭合的 bar"""
        ts = tick["datetime"]
        price = tick["last_price"]
        volume = tick.get("volume", 0)
        # 计算当前 bar 的理论结束时间
        bar_start = (ts // self.duration) * self.duration
        bar_end = bar_start + self.duration

        if self._cur_bar is None:
            # 开始新 bar
            self._cur_bar = Bar(
                symbol=self.symbol,
                datetime=bar_start,
                open=price,
                high=price,
                low=price,
                close=price,
                volume=volume,
                duration=self.duration
            )
            return None

        if ts < bar_end:
            # 仍在同一 bar 内
            self._cur_bar.high = max(self._cur_bar.high, price)
            self._cur_bar.low = min(self._cur_bar.low, price)
            self._cur_bar.close = price
            self._cur_bar.volume += volume
            return None
        else:
            # 当前 bar 闭合，push 并创建新 bar
            closed_bar = self._cur_bar
            self._bars.append(closed_bar)
            # 新建 bar
            self._cur_bar = Bar(
                symbol=self.symbol,
                datetime=bar_start,
                open=price,
                high=price,
                low=price,
                close=price,
                volume=volume,
                duration=self.duration
            )
            return closed_bar

    def get_bars(self, n: int = None) -> List[Bar]:
        bars = list(self._bars)
        if self._cur_bar:
            bars.append(self._cur_bar)
        if n is not None:
            bars = bars[-n:]
        return bars
