# -*- coding: utf-8 -*-
"""
create on 2021-04-22 9:48 上午

author @guorui
"""
import setting
import asyncio

from bots.less_weight_bot import LessWeightBot

bot = LessWeightBot()


async def main():
    bot.on('message')
    await bot.start()


asyncio.run(main())