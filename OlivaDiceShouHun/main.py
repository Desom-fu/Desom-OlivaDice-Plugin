# -*- encoding: utf-8 -*-
'''
@File      :   msgReply.py
@Author    :   Desom-fu
@Contact   :   desom233@outlook.com
@License   :   AGPL
@Copyright :   (C) 2020-2025, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaDiceShouHun
import OlivaDiceCore

class Event(object):
    def init(plugin_event, Proc):
        OlivaDiceShouHun.msgReply.unity_init(plugin_event, Proc)

    def init_after(plugin_event, Proc):
        OlivaDiceShouHun.msgReply.data_init(plugin_event, Proc)

    def private_message(plugin_event, Proc):
        OlivaDiceShouHun.msgReply.unity_reply(plugin_event, Proc)

    def group_message(plugin_event, Proc):
        OlivaDiceShouHun.msgReply.unity_reply(plugin_event, Proc)

    def poke(plugin_event, Proc):
        pass
