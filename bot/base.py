# -*- coding:utf-8 -*-
from config import *
from functools import wraps
from flask import Flask, request
from collections import defaultdict


def _dispatch_decorator(req_type):
    def deco_decorator(self, *types):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            if types:
                for t in types:
                    self._handlers[req_type][t] = wrapper
            return wrapper
        return decorator
    return deco_decorator


class WXBot:

    def __init__(self):
        """
        微信机器人
        """
        self._handlers = defaultdict(dict)
        self._bot = Flask('wxbot')
        self._bot.route('/', methods=['POST'])(self._dispatch)

    @property
    def bot(self):
        """
        返回机器人
        :return:
        """
        return self._bot

    # 装饰器，事件
    on_event = _dispatch_decorator('event_type')

    def _dispatch(self):
        """
        机器人调度核心控制
        1.request中FromId以 '@chatroom' 结尾的为群聊消息，否则为私聊消息
        2.装饰器参数默认为框架的函数名称，群聊在默认的函数名称后加'__chatroom'后缀
        :return:
        """
        # 框架推送的post请求
        req_dict = request.form.to_dict()
        # 获取事件类型
        event_type = req_dict.get('Event')
        # 判断聊天方式：群聊/私聊
        from_id = req_dict.get('FromId')
        # 是否为群聊
        is_chatroom = '@chatroom' in str(from_id)
        if is_chatroom and from_id in config.WX_ROBOT_WORK_GROUP:
            # 群聊，默认route的on_event注解中事件加'__chatroom'后缀
            event_type = event_type+'__chatroom'
            handler = self._handlers.get('event_type').get(event_type)
        else:
            handler = self._handlers.get('event_type').get(event_type)
        if handler:
            return handler(req_dict)

    def run(self, host='0.0.0.0', port=8080, **kwargs):
        self.bot.run(host=host, port=port, **kwargs)

    @staticmethod
    def send_wx_msg(wx_id, msg_content, msg_type, at_user=None):
        """
        发送私聊/群聊消息或者发送原始appmsg xml格式消息
        :param wx_id: wx_id
        :param msg_content: 发送内容
        :param at_user: 是否@接受者，如果@就填写接受者的wxid
        :param msg_type: 默认1或5
        :return:
        """
        assert msg_type == 1 or msg_type == 5, \
            'send_wx_msg方法只支持msg_type=1(发送文本消息) 或者 msg_type=5(发送原始appmsg xml消息)'
        at_user = at_user if at_user else ''
        if msg_type == 1:
            return f'<&&>SendMessage<&>{wx_id}<&>{msg_content}<&>{at_user}<&>{msg_type}'
        elif msg_type == 5:
            return f'<&&>SendAppMsgRaw<&>{wx_id}<&>{msg_content}<&>{msg_type}'


