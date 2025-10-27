# -*- encoding: utf-8 -*-
'''
背包插件主文件
'''

import OlivOS
import OlivaDiceBackpack
import OlivaDiceCore

class Event(object):
    def init(plugin_event, Proc):
        # 初始化插件时调用
        OlivaDiceBackpack.msgReply.unity_init(plugin_event, Proc)

    def init_after(plugin_event, Proc):
        # 在所有插件初始化完成后调用
        OlivaDiceBackpack.msgReply.data_init(plugin_event, Proc)

    def private_message(plugin_event, Proc):
        # 私聊消息处理
        OlivaDiceBackpack.msgReply.unity_reply(plugin_event, Proc)

    def group_message(plugin_event, Proc):
        # 群聊消息处理
        OlivaDiceBackpack.msgReply.unity_reply(plugin_event, Proc)

    def poke(plugin_event, Proc):
        # 戳一戳事件处理
        pass
    
    def menu(plugin_event, Proc):
        # 菜单事件处理
        pass
