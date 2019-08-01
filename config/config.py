# -*- coding:utf-8 -*-
import os
import configparser

cp = configparser.ConfigParser()
cp.read(os.path.dirname(os.path.abspath(__file__))+'/config.ini', encoding='utf-8')

# WX_BOT相关
WX_ROBOT_ID = cp.get('WX_BOT', 'wx_robot_id')
WX_ROBOT_WORK_GROUP = str(cp.get('WX_BOT', 'wx_robot_work_group')).split(',')
WX_ROBOT_KW_REPLY = cp.get('WX_BOT', 'wx_robot_kw_reply')
WX_ROBOT_AT_KW_REPLY = cp.get('WX_BOT', 'wx_robot_at_kw_reply')
MOVIE_SEARCH_URL = cp.get('WX_BOT', 'movie_search_url')
MUSIC_SEARCH_URL = cp.get('WX_BOT', 'music_search_url')
MUSIC_COVER_URL = cp.get('WX_BOT', 'music_cover_url')
MUSIC_DETAIL_URL = cp.get('WX_BOT', 'music_detail_url')
WELCOME_IMG_URL = cp.get('WX_BOT', 'welcome_img_url')
MUSIC_VKEY_URL = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getplaysongvkey05137740976859173&' \
                 'g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&' \
                 'notice=0&platform=yqq.json&needNewCode=0&data=%7B%22req%22%3A%7B%22module' \
                 '%22%3A%22CDN.SrfCdnDispatchServer%22%2C%22method%22%3A%22GetCdnDispatch' \
                 '%22%2C%22param%22%3A%7B%22guid%22%3A%22953482270%22%2C%22calltype%22%3A0%2C%22' \
                 'userip%22%3A%22%22%7D%7D%2C%22req_0%22%3A%7B%22module%22%3A%22vkey.GetVkeyServer' \
                 '%22%2C%22method%22%3A%22CgiGetVkey%22%2C%22param%22%3A%7B%22guid%22%3A%22953482270%22%2C%22' \
                 'songmid%22%3A%5B%22@songmid@%22%5D%2C%22songtype%22%3A%5B0%5D%2C%22uin%22%3A%220%22%2C%22' \
                 'loginflag%22%3A1%2C%22platform%22%3A%2220%22%7D%7D%2C%22comm%22%3A%7B%22uin%22%3A0%2C%22' \
                 'format%22%3A%22json%22%2C%22ct%22%3A24%2C%22cv%22%3A0%7D%7D'
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
# 关键字功能
FUNC_MAP, AT_FUNC_MAP = dict(), dict()
FUNC_KW_LIST, AT_FUNC_KW_LIST = [], []
# 配置聊天关键字功能
for f in str(WX_ROBOT_KW_REPLY).split(';'):
    kvs = str(f).split(':')
    k = kvs[0]
    for kk in k.split(','):
        if kk:
            FUNC_KW_LIST.append(kk)
            FUNC_MAP[kk] = kvs[1]
# 配置at(@)聊天关键字功能
for ff in str(WX_ROBOT_AT_KW_REPLY).split(';'):
    kvs = str(ff).split(':')
    k = kvs[0]
    for kk in k.split(','):
        if kk:
            AT_FUNC_KW_LIST.append(kk)
            AT_FUNC_MAP[kk] = kvs[1]
# func type
FUNC_TYPE_AT = 'at'
FUNC_TYPE_NL = 'normal'



