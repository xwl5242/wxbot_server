# -*- coding:utf-8 -*-

from bot import *

wx_bot = WXBot()
bot = wx_bot.bot


@wx_bot.on_event('ReceiveMessage')
def receive_message(msg):
    """
    私聊
    :param msg: 私聊消息
    :return:
    """
    print(msg)
    content = msg.get('Content')
    sender = msg.get('Sender')
    print(content)
    return wx_bot.send_msg(sender, content)


@wx_bot.on_event('ReceiveMessage__chatroom')
def receive_message_chatroom(msg):
    """
    群聊
    :param msg: 群聊消息
    :return:
    """
    content = msg.get('Content')
    chatroom_id = msg.get('FromId')
    sender_nick = msg.get('SenderNick')
    return wx_bot.send_msg(chatroom_id, f'@{sender_nick} {content}')


if __name__ == '__main__':
    bot.run(host='0.0.0.0', port='8080', debug=True)


