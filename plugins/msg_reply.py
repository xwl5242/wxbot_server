# -*- coding:utf-8 -*-
import config
from plugins.dy import Dy
from plugins.msg import *


def dy_msg(content):
    return 1, Dy().fetch_tv(content)


def menu_msg(content):
    return 1, Menu().menu()


def weather_msg(city):
    return 1, Weather(city).search()


def movie_msg(movie_name):
    """
    电影类 关键词回复
    :param movie_name: 电影名称
    :return:
    """
    movie_message = f'关键词：{movie_name}\n'
    movie_json = Movie(movie_name).search()
    url = ''
    if movie_json.get('rs_code') == 0:
        url = movie_json.get('short_url')
    movie_message = f'{movie_message}观影地址：{url}\n' if url else f'{movie_message}暂无该资源\n'
    movie_message = f'{movie_message}更多精彩视频：http://www.yoviptv.com\n'
    movie_message = f'{movie_message}开启精彩生活 · 趣无止境'
    return 1, movie_message


def music_msg(music_name):
    """
    音乐类 关键词回复
    :param music_name: 音乐名称
    :return:
    """
    return 5, Music(music_name).search()


def msg_reply(content, func_type=config.FUNC_TYPE_NL):
    """
    关键词回复调度方法
    :param content:
    :param func_type:
    :return:
    """
    # 从消息中读取关键字
    content = str(content)
    kw_list, kw_map = [], dict()
    if func_type == config.FUNC_TYPE_NL:
        kw_list, kw_map = config.FUNC_KW_LIST, config.FUNC_MAP
    elif func_type == config.FUNC_TYPE_AT:
        kw_list, kw_map = config.AT_FUNC_KW_LIST, config.AT_FUNC_MAP
    kw = [k for k in kw_list if content.startswith(k)]
    # 是以关键字开头的消息
    if kw and len(kw) > 0:
        kw = kw[0]
        # 除去关键字的 消息内容
        content = str(content[content.index(kw)+len(kw):]).replace(' ', '')
        # 调用相应的处理消息方法
        func = kw_map.get(kw)
        return eval(func)(content)
    else:
        return 1, None


def is_kw_reply(content):
    return len([k for k in config.FUNC_KW_LIST if content.startswith(k)]) > 0


def is_at_kw_reply(content):
    return len([k for k in config.AT_FUNC_KW_LIST if content.startswith(k)]) > 0


