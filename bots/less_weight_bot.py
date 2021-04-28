# -*- coding: utf-8 -*-
"""
create on 2021-04-22 10:13 上午

author @guorui
"""

from wechaty import Wechaty, Message, Room, Contact
from service.search import Judge, Search
import asyncio
import requests


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
        if Judge.is_ask_me(text):
            await msg.say('我在')
        if Judge.is_ask_weather(text):
            text = text.replace("天气", '')
            URL2 = 'https://geoapi.qweather.com/v2/city/lookup?location={}&key=86bae3f81a9c4af9ae7187b23250dffc'.format(
                text)
            resp = requests.get(URL2)
            city = resp.json()
            if int(city.get('code', 0)) != 200:
                await msg.say('找不到这个城市')
            else:
                url = 'https://devapi.qweather.com/v7/weather/now?location={}&key=86bae3f81a9c4af9ae7187b23250dffc'.format(
                    city.get('location', [])[0].get('id'))
                resp = requests.get(url)
                weather = resp.json()
                if int(weather.get('code', 0)) != 200:
                    await msg.say('搜索不到该气温')
                else:
                    msg_ = '{}\n🍁天气：{}\n🍁当前温度为：{}摄氏度\n🍁体感温度为：{}摄氏度'.format(text, weather['now']['text'],
                                                                     weather['now']['temp'],
                                                                     weather['now']['feelsLike'])
                    await msg.say(msg_)
