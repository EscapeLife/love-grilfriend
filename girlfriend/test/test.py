import time
import json

import itchat
from itchat.content import *
import requests


# ------------------------------------------------
# 发送消息给好友
# ------------------------------------------------
friend = itchat.search_friends(nickName='🌵Ms.圆')[0]
print(json.dumps(friend, sort_keys=True, indent=4, separators=(',', ':')))
friend.send('你现在到哪里了呢？什么时候回家呢？')

# ------------------------------------------------
# 发送消息给群聊
# ------------------------------------------------
chatroom = itchat.search_chatrooms(name='怂都弄不成')[0]
print(json.dumps(chatroom, sort_keys=True, indent=4, separators=(',', ':')))
chatroom.send('都干啥呢')





# ------------------------------------------------
# 各类型消息的注册
# 就日常的各种信息进行获取与回复
# ------------------------------------------------
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_friend_reply(msg):
    msg.user.send('%s: %s' % (msg.type, msg.text))

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg.download(msg.fileName)
    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')
    return '@%s@%s' % (typeSymbol, msg.fileName)

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    msg.user.verify()
    msg.user.send('Nice to meet you!')

@itchat.msg_register(TEXT, isGroupChat=True)
def text_chatroom_reply(msg):
    if msg.isAt:
        msg.user.send(u'@%s\u2005I received: %s' % (msg.actualNickName, msg.text))

itchat.auto_login(hotReload=True, enableCmdQR=2)
itchat.run(debug=True, blockThread=True)

# ------------------------------------------------
# 实现微信消息的获取
# 文本对应 itchat.content.TEXT
# 图片对应 itchat.content.PICTURE
# 语音对应 itchat.content.RECORDING
# 名片对应 itchat.content.CARD
# ------------------------------------------------
@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    print(msg['Text'])

itchat.auto_login(hotReload=True, enableCmdQR=2)
itchat.run(debug=True, blockThread=True)

# ------------------------------------------------
# 实现微信消息的发送
# 微信可以发送各类消息/文本/图片/文件等
# ------------------------------------------------
itchat.auto_login(hotReload=True, enableCmdQR=2)
itchat.send(u'测试消息发送', 'filehelper')



# ------------------------------------------------
# 退出及登陆完成后调用特定方法
# ------------------------------------------------
def lc():
    print('### login wechat ###')

def ec():
    print('### logout wechat ###')

itchat.auto_login(hotReload=True, enableCmdQR=2, loginCallback=lc, exitCallback=ec)
time.sleep(3)
itchat.logout()
