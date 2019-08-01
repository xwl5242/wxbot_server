# -*- coding:utf-8 -*-
import json
import requests
from config import *


class Weather:

    def __init__(self, city):
        self.city = city

    def search(self):
        city = self.city
        city = str(city).replace('市区', '').replace('市', '')
        out = ['省', '区', '乡', '村', '国', '镇']
        if len([o for o in out if o in city]) > 0 or len(city) > 5:
            msg = '温馨提示：天气查询时只输入具体城市名称即可查询，如：北京/郑州/正定/磁县/雄县'
        else:
            weather_json = self.__weather(city)
            if weather_json:
                msg = ''
                city = weather_json.get('city')
                msg = f'{msg}所在城市：{city}\n\n'
                day3 = weather_json.get('data')[0:3]
                for i, day in enumerate(day3):
                    msg = f"{msg}{day.get('day')}\t{day.get('week')}\n天气：{day.get('wea')}\n"
                    msg = f"{msg}气温：{day.get('tem2')} ~ {day.get('tem1')}\n"
                    if i == 0:
                        msg = f"{msg}空气质量：{day.get('air_level')}\n{day.get('air_tips')}\n"
                    zwx = day.get('index')[0]
                    msg = f"{msg}{zwx.get('title')}：{zwx.get('level')}\n{zwx.get('desc')}\n"
            msg = f"{msg}\n开启美好生活·趣无止境"
        return msg

    @staticmethod
    def __weather(city):
        """
        天气查询接口的调用，目前只支持根据城市名称查询
        :param city: 城市名称
        :return:
        """
        if city:
            url = config.WEATHER_URL + '?version=v1&city=' + city
            r = requests.get(url=url, )
            return json.loads(r.text)
        return None

