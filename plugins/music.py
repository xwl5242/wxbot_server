# -*- coding:utf-8 -*-
import json
import config
import random
import requests
from plugins.msg_xmls import get_music_xml


class Music:
    def __init__(self, music_name):
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
        music_xml = ''
        headers = {'User-Agent': random.choice(self.uas)}
        r = requests.get(url=config.MUSIC_URL+self.music_name, headers=headers)
        qq_song = json.loads(r.text.replace('callback(', '')[:-1])
        if qq_song.get('code') == 0:
            songs = dict(qq_song.get('data').get('song'))
            if songs.get('curnum') > 0:
                song = dict(list(songs.get('list'))[0])
                if song:
                    albumid = int(song.get('albumid'))
                    songid = song.get('songid')
                    songmid = song.get('songmid')
                    songname = song.get('songname')
                    data_url = self.__get_data_url(songmid)
                    singer = song.get('singer')[0].get('name')
                    cover = self.__get_cover(albumid)
                    music_xml = get_music_xml(songname, singer, cover, data_url, f'http://y.qq.com/#type=song&id={songid}')
        return music_xml

    @staticmethod
    def __get_data_url(song_mid):
        vkey_url = config.VKEY_URL.replace('@songmid@', song_mid)
        res = requests.get(url=vkey_url)
        res02 = json.loads(res.text)
        vkey = res02["req_0"]["data"]["midurlinfo"][0]["purl"]
        return 'http://ws.stream.qqmusic.qq.com/'+vkey

    @staticmethod
    def __get_cover(album_id):
        cover_url = config.COVER_URL.replace('@albumid1@', str(album_id % 100))\
            .replace('@albumid2@', str(album_id))
        return cover_url


if __name__ == '__main__':
    Music('像鱼').get_cover(5540670)


