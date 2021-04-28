# -*- coding: utf-8 -*-
"""
create on 2021-04-25 2:55 下午

author @guorui
"""
# DB={
#     'connections': {
#         # Dict format for connection
#         'default': {
#             'engine': 'tortoise.backends.aiomysql',
#             'credentials': {
#                 'host': 'localhost',
#                 'port': '3306',
#                 'user': 'root',
#                 'password': 'root',
#                 'database': 'mydb',
#             }
#         },
#         # Using a DB_URL string
#     },
#     'apps': {
#         'models': {
#             'models': ['__main__'],
#             # If no default_connection specified, defaults to 'default'
#             'default_connection': 'default',
#         }
#     },
#     'routers': ['path.router1', 'path.router2'],
#     'use_tz': False,
#     'timezone': 'UTC'
# }
import os

os.environ.update({'WECHATY_PUPPET_SERVICE_TOKEN': 'puppet_paimon_480e529828599ac61c8f125d99fd6db0'})
DB ='mysql://root:root@49.232.145.52:3306/weight'
TORTOISE_ORM = {
    "connections": {"default": DB},
    "apps": {
        "models": {
            "models": ["aerich.models", "models.models"],
            "default_connection": "default",
        },
    },
}