#!/usr/bin/env python
#  -*- coding: utf-8 -*-
"""
@ProjectName: homalos-lite
@FileName   : channel.py
@Date       : 2026/5/7 14:06
@Author     : Lumosylva
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: 单向数据流通道
"""
import asyncio
from typing import Any

class HmlChan:
    """基于 asyncio.Queue 的单向管道，用于组件间解耦"""
    def __init__(self, maxsize: int = 0):
        self._queue: asyncio.Queue = asyncio.Queue(maxsize=maxsize)

    async def put(self, item: Any) -> None:
        await self._queue.put(item)

    async def get(self) -> Any:
        return await self._queue.get()

    def empty(self) -> bool:
        return self._queue.empty()

    def qsize(self) -> int:
        return self._queue.qsize()
