# -*- encoding: utf-8 -*-
'''
@File      :   main.py
@Author    :   Desom-fu
@Contact   :   Desom233@outlook.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaDicePuke
import OlivaDiceCore

class Event(object):
    def init(plugin_event, Proc):
        OlivaDicePuke.msgReply.unity_init(plugin_event, Proc)

    def init_after(plugin_event, Proc):
        OlivaDicePuke.msgReply.data_init(plugin_event, Proc)

    def private_message(plugin_event, Proc):
        OlivaDicePuke.msgReply.unity_reply(plugin_event, Proc)

    def group_message(plugin_event, Proc):
        OlivaDicePuke.msgReply.unity_reply(plugin_event, Proc)

    def poke(plugin_event, Proc):
        pass
