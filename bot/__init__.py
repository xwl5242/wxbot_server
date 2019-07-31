# -*- coding:utf-8 -*-
from functools import wraps
from flask import Flask, request
from collections import defaultdict
from bot.bdbot import BDUnitBot


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
        self._handlers = defaultdict(dict)
        self._bot = Flask('wxbot')
        self._bot.route('/', methods=['POST'])(self._dispatch)

    @property
    def bot(self):
        return self._bot

    on_event = _dispatch_decorator('event_type')

    def _dispatch(self):
        req_dict = request.form.to_dict()
        event_type = req_dict.get('Event')
        # FromId以 '@chatroom' 结尾的为群聊，否则为私聊
        # 私聊中所有event为框架默认的Event，群聊中所有的event自定义为在私聊后加‘__chatroom’
        # 私聊默认event为ReceiveMessage，所以群聊event为ReceiveMessage__chatroom
        from_id = req_dict.get('FromId')
        is_chatroom = str(from_id).endswith('@chatroom')    # 是否群聊
        if is_chatroom:
            # 群聊，默认route的on_event注解中事件+__chatroom后缀
            event_type = event_type+'__chatroom'
        handler = self._handlers.get('event_type').get(event_type)
        if handler:
            return handler(req_dict)

    def run(self, host='0.0.0.0', port=8080, **kwargs):
        self.bot.run(host=host, port=port, **kwargs)

    def send_msg(self, wxid, msg_content, msg_type, at_user=None):
        """
        发送私聊消息或者群聊消息
        :param wxid: 接受者wxid
        :param msg_content: 发送内容
        :param at_user: 是否@接受者，如果@就填写接受者的wxid
        :param msg_type: 默认1
        :return:
        """
        at_user = at_user if at_user else ''
        if msg_type == 1:
            return f'<&&>SendMessage<&>{wxid}<&>{msg_content}<&>{at_user}<&>{msg_type}'
        elif msg_type == 5:
            return f'<&&>SendAppMsgRaw<&>{wxid}<&>{msg_content}<&>{msg_type}'


