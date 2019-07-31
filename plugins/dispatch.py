# -*- coding:utf-8 -*-
import config
from plugins.movie import Movie


def movie_msg(movie_name):
    movie = Movie(movie_name).search()


def music_msg(music_msg):
    music = ''


def dispatch(content):
    # 从消息中读取关键字
    content = str(content)
    kw = [k for k in config.FUNC_KW_LIST if content.startswith(k)]
    # 是以关键字开头的消息
    if kw and len(kw) > 0:
        kw = kw[0]
        # 除去关键字的 消息内容
        content = str(content[content.index(kw):]).replace(' ', '')
        # 调用相应的处理消息方法
        return config.FUNC_MAP.get(kw)(content)


