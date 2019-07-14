# -*- coding: utf-8 -*-
"""
检测是否有删除自己或把自己拉入黑名单的朋友
原理: 将好友拉入群聊时，非好友和黑名单好友不会被拉入群聊
隐蔽: 群聊在第一次产生普通消息时才会被除创建者以外的人发现的(系统消息不算普通消息)
"""

import itchat


class ConfirmFriend:
    """自动检测好友关系"""
    def __init__(self, chatroom=None, chatroom_name='friends'):
        self.chatroom = chatroom
        self.chatroom_name = chatroom_name
        self.status_dict = {3: '该好友已经将你加入黑名单', 4: '该好友已经将你删除'}

    def get_chatroom(self):
        """获取群组信息"""
        if self.chatroom is None:
            itchat.get_chatrooms(update=True)
            chatrooms = itchat.search_chatrooms(self.chatroom)
            if chatrooms:
                return chatrooms[0]
            room = itchat.create_chatroom(itchat.get_friends()[1:4], topic=self.chatroom_name)
            if room['BaseResponse']['ErrMsg'] == '':
                self.chatroom = {'UserName': room['ChatRoomName']}
                return self.chatroom
        return self.chatroom

    def get_friend_status(self):
        """获取好友状态"""
        own_account = itchat.get_friends(update=True)[0]
        friends_total_number = len(itchat.get_friends())
        for num in range(friends_total_number):
            friend = itchat.get_friends()[num]
            if friend['UserName'] == own_account['UserName']:
                return "This account is not checked for my account."
            if itchat.search_friends(userName=friend['UserName']) is None:
                return "The user is not exist."

            chatroom = self.chatroom or self.get_chatroom()
            if chatroom is None:
                return '无法自动创建群聊请手动创建 | 创建后请将群聊保存到通讯录'
            room = itchat.add_member_into_chatroom(chatroom['UserName'], [friend])
            if room['BaseResponse']['ErrMsg'] == '':
                friend_status = room['MemberList'][0]['MemberStatus']
                itchat.delete_member_from_chatroom(chatroom['UserName'], [friend])
                return self.status_dict.get(friend_status, '该好友仍旧与你是好友关系')
            return u'无法获取好友状态，预计已经达到接口调用限制。'


if __name__ == '__main__':
    itchat.auto_login(hotReload=True, enableCmdQR=2)
    CONFIRM = ConfirmFriend()
    CONFIRM.get_friend_status()
