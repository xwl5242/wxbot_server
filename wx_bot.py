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
    r_type = str(msg.get('Type'))
    if r_type == '10002':
        # 该机器人只做入群欢迎语功能
        from_id = msg.get('from_id')
        content = str(msg.get('content'))
        start_str, end_str = '<nickname>', '</nickname>'
        s_index, e_index = content.index(start_str) + len(start_str), content.index(end_str)
        sender = content[s_index:e_index]
        sender = sender.replace('<![CDATA[', '').replace(']]>', '')
        if '加入群聊' in content:
            return wx_bot.send_wx_msg(from_id, f'@{sender}\n欢迎加入，您可以@Coco机器人，发送"菜单"，获取群聊功能\n祝您使用愉快！', 1)
        else:
            xml = """
            <appmsg appid="wx485a97c844086dc9"  sdkver="0">
                <title>分享测试</title>
                <des>分享描述</des>
                <type>5</type>
                <content>1111</content>
                <url>http://v6-dy.ixigua.com/d491f9f4492cb4c3e22cd8d07042e0e0/5d42a8bd/video/m/2206858e5ccc40143ba85542da908a852be116294de700005fe0a6363efc/?rc=MzhubnZmc3d0bjMzZ2kzM0ApdSk1ODo2NDQ1MzM0ODQzMzQ1b2U7M2Y0OWdmOGRmOTYzaWlAaUBoNHYpQGczdilAZjs0QGpwcjAvZy4yL18tLV8tL3NzOmkwMTQ2Li4xLS4zMTIuNTYtOiNiMWE1XjBhNV4xMC1gYi0xYSNvIzphLW8jOmAtbyMvLl4%3D</url>
                <thumburl>https://p9-dy.byteimg.com/aweme/1080x1080/240c40006daeef91f2bd5.jpeg</thumburl>
            </appmsg>
            """
            return wx_bot.send_wx_msg(from_id, xml, 5)
    return ''


if __name__ == '__main__':
    bot.run(host='0.0.0.0', port='8080', debug=False)


