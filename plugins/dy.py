# -*- coding:utf-8 -*-
import json
import config
import requests
from lxml import etree


class Dy:

    def fetch_tv(self, url):
        msg = '抖音去水印\n'
        r = requests.get(config.DY_JX_URL+url)
        root = etree.HTML(r.content.decode('utf-8'))
        urls = root.xpath('//textarea/text()')
        if urls and len(urls) == 2:
            tv_url = dict(self.sina_short_url(urls[0])).get('short_url')
            # mp3_url = self.sina_short_url(urls[1])
            msg = f'{msg}视频分享地址：{url}\n视频下载地址：{tv_url}\n'
            # msg = f'{msg}视频伴音地址：{mp3_url}\n'
        return f'{msg}开始美好生活 · 趣无止境'

    @staticmethod
    def sina_short_url(long_url):
        """
        新浪短地址接口调用
        :param long_url: 要转换为短地址的长地址
        :return:
        """
        r = requests.get(f'{config.SINA_URL}?appkey={config.SINA_KEY}&long_url={long_url}')
        return json.loads(r.text)




