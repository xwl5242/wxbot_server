# -*- coding:utf-8 -*-
import json
import config
import requests
from urllib.parse import quote


class Movie:

    def __init__(self, movie_name):
        self.movie_name = quote(movie_name)

    def search(self):
        long_url = f'{config.TV_SEARCH_URL}{self.movie_name}'
        return Movie.sina_short_url(long_url)

    @staticmethod
    def sina_short_url(long_url):
        """
        新浪短地址接口调用
        :param long_url: 要转换为短地址的长地址
        :return:
        """
        r = requests.get(f'{config.SINA_URL}?appkey={config.SINA_KEY}&long_url={long_url}')
        return json.loads(r.text)

