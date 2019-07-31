# -*- coding:utf-8 -*-
import config
from plugins.movie import Movie
from plugins.music import Music


def movie_msg(movie_name):
    movie_message = f'关键词：{movie_name}\n'
    movie_json = Movie(movie_name).search()
    url = ''
    if movie_json.get('rs_code') == 0:
        url = movie_json.get('short_url')
    movie_message = f'{movie_message}观影地址：{url}\n' if url else f'{movie_message}暂无该资源\n'
    movie_message = f'{movie_message}更多精彩视频：http://www.yoviptv.com\n'
    movie_message = f'{movie_message}开启精彩生活 · 趣无止境'
    return 1, movie_message


def music_msg(music_msg):
    music = Music(music_msg).search()
    return 5, music


def dispatch(content):
    # 从消息中读取关键字
    content = str(content)
    kw = [k for k in config.FUNC_KW_LIST if content.startswith(k)]
    # 是以关键字开头的消息
    if kw and len(kw) > 0:
        kw = kw[0]
        # 除去关键字的 消息内容
        content = str(content[content.index(kw)+len(kw):]).replace(' ', '')
        # 调用相应的处理消息方法
        func = config.FUNC_MAP.get(kw)
        return eval(func)(content)


def is_kw_reply(content):
    return len([k for k in config.FUNC_KW_LIST if content.startswith(k)]) > 0

