# -*- coding: utf-8 -*-
"""
一个消息群发助手

Usage:
    itchat.auto_login(hotReload=True, enableCmdQR=2)
    MASS = MassMSG()
    MASS.send_all_friends_msg()
    MASS.send_special_group_msg()
"""

import time
import itchat


class MassMSG:
    """消息群发助手"""
    def __init__(self, greetings='Happy New Year', chatroom_name='mass_group'):
        self.greetings = greetings
        self.chatroom_name = chatroom_name

    def send_all_friends_msg(self):
        """给所有好友发送消息"""
        # 获取的好友列表首位是自己
        friends_list = itchat.get_friends(update=True)[1:]
        for friend in friends_list:
            # 如果用于演示则使用print方法
            itchat.send(f'{self.greetings} | {friend["NickName"]}', friend['UserName'])
            print(f'>>> send {friend["NickName"]} is finished.')
            time.sleep(3)

    def send_special_group_msg(self):
        """给指定群组内的成员发送消息"""
        itchat.get_friends(update=True)
        chatrooms = itchat.search_chatrooms(name=self.chatroom_name)
        if chatrooms is None:
            print(f'The {self.chatroom_name} is not found.')
        else:
            chatroom = itchat.update_chatroom(chatrooms[0]['UserName'])
            for friend in chatroom['MemberList']:
                friend = itchat.search_friends(userName=friend['UserName'])
                # 如果用于演示则使用print方法
                itchat.send(f'{self.greetings} | {friend["NickName"]}', friend['UserName'])
                print(f'>>> send {friend["NickName"]} is finished.')
                time.sleep(3)
