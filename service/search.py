# -*- coding: utf-8 -*-
"""
create on 2021-04-25 2:34 下午

author @guorui
"""
import time
import re
from tortoise import Tortoise

import setting
from models import models
from wechaty import Wechaty, Message, Room, Contact


async def init_DB():
    await Tortoise.init(db_url=setting.DB, modules={"models": ["models.models"]})
    await Tortoise.generate_schemas()


class Judge:
    @staticmethod
    def is_ask_self_weight(msg):
        if msg == '查询记录':
            return True
        return False

    @staticmethod
    def is_ask_self_login(msg):
        if msg == '注册':
            return True
        return False

    @staticmethod
    def is_ask_tag_weight(msg):
        a = re.match('目标体重', msg)
        if a:
            return True
        return False

    @staticmethod
    def is_ask_present_weight(msg):
        a = re.match('当前体重', msg)
        if a:
            return True
        return False


class Search:
    @staticmethod
    async def search_weight(user: Contact):
        await init_DB()
        new_user = await models.Users.filter(wechat_num=user.contact_id).first()
        user_weight = await models.User_Weight.filter(user=new_user).first()
        weight_report = await models.Weight.filter(id=user_weight.weight_report_id).first()
        return '🥳{}🥳\n☘{}☘\n🌼目标体重:{}\n🤯当前体重:{}\n🌵最近体重变化:{}\n🏃🏻总计体重变化:{}\n🍁>加油哦,坚持就是胜利<🍁'.format(new_user.name,
                                                                                                         time.strftime(
                                                                                                             "%Y年 %m月 %d日 ",
                                                                                                             time.localtime()),
                                                                                                         weight_report.tag_weight,
                                                                                                         weight_report.present_weight,
                                                                                                         weight_report.once_change,
                                                                                                         weight_report.week_change)

    @staticmethod
    async def create_self(user: Contact):
        await init_DB()
        new_user, created = await models.Users.get_or_create(name=user.name, wechat_num=user.contact_id)
        if created:
            weight = await models.Weight.create(tag_weight=100)
            user_weight, created = await models.User_Weight.get_or_create(user=new_user, weight_report=weight)
            return user
        return created

    @staticmethod
    async def update_weight(user: Contact, **kwargs):
        await init_DB()
        print(kwargs)
        new_user = await models.Users.filter(wechat_num=user.contact_id).first()
        user_weight = await models.User_Weight.filter(user=new_user).first()
        print(new_user.name)
        weight_report = await models.Weight.filter(id=user_weight.weight_report_id).first()
        present = weight_report.present_weight
        once = weight_report.once_change
        await weight_report.update_from_dict(kwargs)
        weight_report.once_change = round(present - weight_report.present_weight, 1)
        weight_report.week_change = round(once + weight_report.once_change, 1)
        await weight_report.save()
        msg = '🥳{}🥳\n☘{}☘\n🌼目标体重:{}\n🤯当前体重:{}\n🌵最近体重变化:{}\n🏃🏻总计体重变化:{}\n🍁>加油哦,坚持就是胜利<🍁'.format(new_user.name,
                                                                                                        time.strftime(
                                                                                                            "%Y年 %m月 %d日 ",
                                                                                                            time.localtime()),
                                                                                                        weight_report.tag_weight,
                                                                                                        weight_report.present_weight,
                                                                                                        weight_report.once_change,
                                                                                                        weight_report.week_change)
        return msg
