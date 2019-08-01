# -*- coding:utf-8 -*-
import config
from bot import *
from plugins.msg_reply import *

wx_bot = WXBot()
bot = wx_bot.bot


@wx_bot.on_event('ReceiveMessage')
def receive_message(msg):
    """
    私聊
    :param msg: 私聊消息
    :return:
    """
    content = msg.get('Content')
    sender = msg.get('Sender')
    if is_kw_reply(content):
        msg_type, reply = msg_reply(content)
    else:
        msg_type = 1
        uid, reply = BDUnitBot.chat(sender, content)
    return wx_bot.send_wx_msg(sender, reply, msg_type)


@wx_bot.on_event('ReceiveMessage__chatroom')
def receive_message_chatroom(msg):
    """
    群聊
    :param msg: 群聊消息
    :return:
    """
    at_list = msg.get('AtList')  # @消息
    content = msg.get('Content')
    chatroom_id = msg.get('FromId')
    sender_nick = str(msg.get('SenderNick')).split('@')[0].replace('在群聊中', '')
    if config.WX_ROBOT_ID in at_list:
        msg_type = 1
        # 群聊中有人@自己，@自己开启百度闲聊
        uid, reply = BDUnitBot.chat(chatroom_id, content)
    else:
        # 关键字回复
        msg_type, reply = msg_reply(content)
    if reply:
        return wx_bot.send_wx_msg(chatroom_id, f'@{sender_nick}\n{reply}', msg_type)
    return ''


if __name__ == '__main__':
    bot.run(host='0.0.0.0', port='8080', debug=False)


