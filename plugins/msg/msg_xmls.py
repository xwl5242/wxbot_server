# -*- coding:utf-8 -*-
img_xml = """
<msg>
    <img length="6503" hdlength="0" />
    <commenturl>@url@</commenturl>
</msg>
"""
music_xml = """
<appmsg appid="wx485a97c844086dc9" sdkver="0">
    <title>@song@</title>
    <des>@singer@</des>
    <action></action>
    <type>3</type>
    <showtype>0</showtype>
    <mediatagname></mediatagname>
    <messageext></messageext>
    <messageaction></messageaction>
    <content></content>
    <contentattr>0</contentattr>
    <url>@url@</url>
    <lowurl></lowurl>
    <dataurl>@dataurl@</dataurl>
    <lowdataurl></lowdataurl>
    <appattach>
        <totallen>0</totallen>
        <attachid></attachid>
        <emoticonmd5></emoticonmd5>
        <fileext></fileext>
    </appattach>
    <extinfo></extinfo>
    <sourceusername></sourceusername>
    <sourcedisplayname></sourcedisplayname>
    <commenturl></commenturl>
    <thumburl>@cover@</thumburl>
    <md5></md5>
</appmsg>
"""


def get_music_xml(song, singer, cover_url, data_url, url):
    """
    获取微信音乐类型消息的appmsg
    :param song: 歌曲名称
    :param singer: 歌手
    :param cover_url: 封面图片地址
    :param data_url: 歌曲地址
    :param url: 歌曲详情地址
    :return:
    """
    return music_xml.replace('@url@', url).replace('@cover@', cover_url)\
        .replace('@song@', song).replace('@singer@', singer).replace('@dataurl@', data_url)


