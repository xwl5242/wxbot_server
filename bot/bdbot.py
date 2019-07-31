# -*- coding:utf-8 -*-
import uuid
import time
import json
import config
import random
import requests
from plugins import MRedis


class BDUnitBot:
    REDIS_BD_ACCESS_TOKEN_KEY = 'bd_access_token'
    """
    百度UNIT，闲聊机器人
    """
    @staticmethod
    def __oauth():
        """
        请求获取access_token
        :return:
        """
        # header
        header = {'Content-Type': 'application/json;charset=UTF-8', 'Connection': 'close'}
        # 请求参数
        data = {'grant_type': 'client_credentials',
                'client_id': config.BOT_API_KEY,
                'client_secret': config.BOT_API_SECRET
                }
        # 请求
        r = requests.post(url=config.BOT_OAUTH, headers=header, data=data)
        r = json.loads(r.text)
        # 获取access_token
        access_token = r.get('access_token')
        expires_in = r.get('expires_in')
        last_time = int(time.time())
        # 存入redis
        MRedis.set_json(BDUnitBot.REDIS_BD_ACCESS_TOKEN_KEY,
                        {'last_time': last_time, 'access_token': access_token, 'expires_in': expires_in})
        return access_token

    @staticmethod
    def access_token():
        """
        获取access_token
        :return:
        """
        c_access_token = MRedis.get_json(BDUnitBot.REDIS_BD_ACCESS_TOKEN_KEY)
        if c_access_token:
            if int(time.time()) - (int(c_access_token['last_time'])+int(c_access_token['expires_in'])/30) < 0:
                return c_access_token['access_token']
            else:
                return BDUnitBot.__oauth()
        else:
            return BDUnitBot.__oauth()

    @staticmethod
    def chat(uid, content):
        """
        闲聊
        :param uid: 用户唯一id(wxid)
        :param content: 用户的消息
        :return:
        """
        # 先查询用户对话是否失效，默认三分钟无对话即为失效
        session_ = MRedis.get_json(uid)
        if session_:
            lct = int(session_['last_chat_time'])
            if (int(time.time()) - lct) > 3*60:
                session_id = ''
            else:
                session_id = session_['session_id']
        else:
            session_id = ''
        # 调用百度UNIT的access_token
        access_token = BDUnitBot.access_token()
        # 闲聊
        return BDUnitBot.__chat(uid, session_id, content, access_token)

    @staticmethod
    def __chat(uid, session_id, content, access_token):
        """
        聊天
        :param uid: 用户唯一id
        :param session_id: 对话session_id
        :param content: 对话内容
        :param access_token: 请求access_token
        :return:
        """
        url = config.BOT_URL + '?access_token=' + access_token
        data = {
            'log_id': str(uuid.uuid4()),
            'version': '2.0',
            'service_id': config.BOT_ID,
            'session_id': session_id,
            'request': {
                'query': content,
                'user_id': uid
            }
        }
        r = requests.post(url=url, headers={'Content-Type': 'application/json'}, data=json.dumps(data).encode('utf-8'))
        resp = json.loads(r.text)
        if resp:
            if resp['error_code'] == 0:
                # 闲聊回复成功
                resp = resp['result']
                resp_list = list(resp['response_list'])
                if resp_list and len(resp_list) > 0:
                    action_list = list(resp_list[0]['action_list'])
                    if action_list and len(action_list) > 0:
                        MRedis.set_json(uid, {'session_id': resp['session_id'], 'last_chat_time': int(time.time())})
                        reply_ = random.choice(action_list).get('say')
                        return uid, reply_
        return uid, None

