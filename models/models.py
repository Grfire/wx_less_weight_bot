# -*- coding: utf-8 -*-
"""
create on 2021-04-25 2:47 下午

author @guorui
"""
from tortoise import Model, fields


class Users(Model):
    id = fields.IntField(pk=True, )
    name = fields.CharField(50)
    wechat_num = fields.CharField(50)

    def __str__(self):
        return f"User {self.id}: {self.name}"


class Weight(Model):
    id = fields.IntField(pk=True)
    tag_weight = fields.FloatField(max_length=100, default=0.0)
    present_weight = fields.FloatField(max_length=100, default=0.0)
    once_change = fields.FloatField(max_length=100, default=0.0)
    week_change = fields.FloatField(max_length=100, default=0.0)


class User_Weight(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(model_name='models.Users', related_name='events')
    weight_report = fields.ForeignKeyField(model_name='models.Weight', related_name='events')
    create_at = fields.DatetimeField(auto_now=True)

    # async def get_weight_report(self):
    #     await self.get()
