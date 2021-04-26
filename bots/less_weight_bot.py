# -*- coding: utf-8 -*-
"""
create on 2021-04-22 10:13 上午

author @guorui
"""

import os
from datetime import datetime
from typing import List

from tortoise import Tortoise

from wechaty import Wechaty, Message, Room, Contact
from service.search import Judge, Search
import asyncio


class LessWeightBot(Wechaty):
    async def on_message(self, msg: Message):
        user = msg.talker()
        text = msg.text()
        if Judge.is_ask_self_weight(text):
            msg_ = await Search.search_weight(user)
            await msg.say(msg_)
        if Judge.is_ask_self_login(text):
            user = await Search.create_self(user)
            if user:
                await msg.say('成功,欢迎🥳{}'.format(user.name))
        if Judge.is_ask_tag_weight(text):
            text = text.replace('：', ':')
            text = text.split(':')
            msg_ = await Search.update_weight(user, tag_weight=float(text[-1]))
            await msg.say(msg_)
        if Judge.is_ask_present_weight(text):
            text = text.replace('：', ':')
            text = text.split(':')
            msg_ = await Search.update_weight(user, present_weight=float(text[-1]))
            await msg.say(msg_)



