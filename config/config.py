# -*- coding:utf-8 -*-
import os
import configparser


cp = configparser.ConfigParser()
cp.read(os.path.dirname(os.path.abspath(__file__))+'/config.ini', encoding='utf-8')

# access_token, secret
SECRET = cp.get('WX_BOT', 'secret')
WX_ROBOT_ID = cp.get('WX_BOT', 'wx_robot_id')

# 视频查询接口地址
TV_SEARCH_URL = str(cp.get('TV_SEARCH_URL', 'tv_search_url'))

# 关键字功能
FUNCS = str(cp.get('GROUP_FUNC', 'funcs')).split(';')
FUNC_MAP = dict()
FUNC_KW_LIST = []
for f in FUNCS:
    kvs = str(f).split(':')
    k = kvs[0]
    for kk in k:
        FUNC_KW_LIST.append(kk)
        FUNC_MAP[kk] = kvs[1]

# 新浪短地址服务
SINA_URL = str(cp.get('SHORT_URL', 'sina_url'))
SINA_KEY = str(cp.get('SHORT_URL', 'sina_appkey'))

# 天气预报接口url
WEATHER_URL = str(cp.get('WEATHER', 'weather_url'))

# 百度机器人
BOT_URL = str(cp.get('BD_BOT', 'bot_url'))
BOT_OAUTH = str(cp.get('BD_BOT', 'oauth_url'))
BOT_API_KEY = str(cp.get('BD_BOT', 'apikey'))
BOT_API_SECRET = str(cp.get('BD_BOT', 'apisecret'))
BOT_ID = str(cp.get('BD_BOT', 'service_id'))

