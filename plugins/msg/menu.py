# -*- coding:utf-8 -*-
import config
from plugins.msg.msg_xmls import img_xml

class Menu:

    @staticmethod
    def menu():
        menu_str = """
①影视 | 影视搜索功能
②音乐 | 音乐搜索功能 
③天气 | 天气搜索功能
        
① 回复'电影/电视剧/综艺/动漫+影视名称'
② 回复'音乐/歌曲+歌曲名称'
③ 回复'天气+城市名称'

更多精彩功能，正在路上，敬请期待
        """
        return menu_str


class WelCome:

    @staticmethod
    def welcome():
        return img_xml.replace('@url@', config.WELCOME_IMG_URL)


