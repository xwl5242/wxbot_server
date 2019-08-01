# -*- coding:utf-8 -*-
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
    sender = msg.get('Sender')
    chatroom_id = msg.get('FromId')
    sender_nick = str(msg.get('SenderNick')).split('@')[0].replace('在群聊中', '')
    if config.WX_ROBOT_ID in at_list:
        msg_type = 1
        # 群聊中有人@自己，@自己开启@关键字回复或者百度闲聊
        content = content[content.index(' ')+1:]
        if is_at_kw_reply(content):
            msg_type, reply = msg_reply(content, 'at')
        else:
            uid, reply = BDUnitBot.chat(sender, content)
    else:
        # 关键字回复
        msg_type, reply = msg_reply(content)
    if reply:
        return wx_bot.send_wx_msg(chatroom_id, f'@{sender_nick}\n{reply}', msg_type)
    return ''


@wx_bot.on_event('ReceiveSysMsg')
def receive_sys_msg_chatroom(msg):
    """
    系统消息，入群，退群
    :param msg:
    :return:
    """
    print(msg)
    r_type = str(msg.get('Type'))
    if r_type == '10002':
        from_id = msg.get('from_id')
        content = str(msg.get('content'))
        start, end = '<nickname>', '</nickname>'
        content = content[content.index(start)+len(start), content.index(end)]
        sender = content.replace('<![CDATA[', '').replace(']', '').replace('>', '').replace('<', '')
        if '加入群聊' in content:
            return wx_bot.send_wx_msg(from_id, f'@{sender}\n欢迎加入，您可以@Coco机器人，发送菜单，获取群聊功能\n祝您使用愉快！', 1)
    return ''


if __name__ == '__main__':
    bot.run(host='0.0.0.0', port='8080', debug=False)


