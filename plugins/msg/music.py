# -*- coding:utf-8 -*-
import json
import config
import random
import requests
from plugins.msg.msg_xmls import get_music_xml


class Music:
    def __init__(self, music_name):
        """
        qq音乐点歌功能
        :param music_name:
        """
        self.uas = [
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
        ]
        self.music_name = music_name

    def search(self):
        """
        搜索QQ音乐
        :return:
        """
        music_xml = ''
        headers = {'User-Agent': random.choice(self.uas)}
        r = requests.get(url=config.MUSIC_SEARCH_URL+self.music_name, headers=headers)
        # QQ音乐搜索结果
        qq_song = json.loads(r.text.replace('callback(', '')[:-1])
        if qq_song.get('code') == 0:
            songs = dict(qq_song.get('data').get('song'))
            if songs.get('curnum') > 0:
                # 搜索到歌曲
                song = dict(list(songs.get('list'))[0])
                if song:
                    album_id, song_id, song_mid, song_name = int(song.get('albumid')), \
                                                         song.get('songid'), song.get('songmid'), song.get('songname')
                    # 获取歌曲播放地址
                    data_url = self.__get_data_url(song_mid)
                    # 获取歌手名字
                    singer = song.get('singer')[0].get('name')
                    # 获取封面
                    cover = self.__get_cover(album_id)
                    # 获取微信返回音乐类型消息appmsg xml
                    music_xml = get_music_xml(song_name, singer, cover, data_url, f'{config.MUSIC_DETAIL_URL}{song_id}')
        return music_xml

    @staticmethod
    def __get_data_url(song_mid):
        """
        获取音乐的播放地址
        :param song_mid:
        :return:
        """
        vkey_url = config.MUSIC_VKEY_URL.replace('@songmid@', song_mid)
        r = requests.get(url=vkey_url)
        vkey_json = json.loads(r.text)
        vkey = vkey_json["req_0"]["data"]["midurlinfo"][0]["purl"]
        return 'http://ws.stream.qqmusic.qq.com/'+vkey

    @staticmethod
    def __get_cover(album_id):
        """
        获取音乐的封面图片地址
        :param album_id:
        :return:
        """
        cover_url = config.MUSIC_COVER_URL.replace('@albumid1@', str(album_id % 100))\
            .replace('@albumid2@', str(album_id))
        return cover_url



