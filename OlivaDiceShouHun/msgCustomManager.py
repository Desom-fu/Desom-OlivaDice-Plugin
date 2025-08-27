# -*- encoding: utf-8 -*-
'''
@File      :   msgCustomManager.py
@Author    :   Desom-fu
@Contact   :   desom233@outlook.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaDiceCore
import OlivaDiceShouHun
import os
import json

has_NativeGUI = False
try:
    import OlivaDiceNativeGUI
    has_NativeGUI = True
except ImportError:
    has_NativeGUI = False

def initMsgCustom(bot_info_dict):
    for bot_info_dict_this in bot_info_dict:
        if bot_info_dict_this not in OlivaDiceCore.msgCustom.dictStrCustomDict:
            OlivaDiceCore.msgCustom.dictStrCustomDict[bot_info_dict_this] = {}
        for dictStrCustom_this in OlivaDiceShouHun.msgCustom.dictStrCustom:
            if dictStrCustom_this not in OlivaDiceCore.msgCustom.dictStrCustomDict[bot_info_dict_this]:
                OlivaDiceCore.msgCustom.dictStrCustomDict[bot_info_dict_this][dictStrCustom_this] = OlivaDiceShouHun.msgCustom.dictStrCustom[dictStrCustom_this]
        if has_NativeGUI:
            for dictStrCustomNote_this in OlivaDiceShouHun.msgCustom.dictStrCustomNote:
                if dictStrCustomNote_this not in OlivaDiceNativeGUI.msgCustom.dictStrCustomNote:
                    OlivaDiceNativeGUI.msgCustom.dictStrCustomNote[dictStrCustomNote_this] = OlivaDiceShouHun.msgCustom.dictStrCustomNote[dictStrCustomNote_this]
        for dictHelpDoc_this in OlivaDiceShouHun.msgCustom.dictHelpDocTemp:
            if dictHelpDoc_this not in OlivaDiceCore.helpDocData.dictHelpDoc[bot_info_dict_this]:
                OlivaDiceCore.helpDocData.dictHelpDoc[bot_info_dict_this][dictHelpDoc_this] = OlivaDiceShouHun.msgCustom.dictHelpDocTemp[dictHelpDoc_this]
    OlivaDiceCore.msgCustom.dictStrConst.update(OlivaDiceShouHun.msgCustom.dictStrConst)
    OlivaDiceCore.msgCustom.dictGValue.update(OlivaDiceShouHun.msgCustom.dictGValue)
    OlivaDiceCore.msgCustom.dictTValue.update(OlivaDiceShouHun.msgCustom.dictTValue)
    if has_NativeGUI:
        OlivaDiceNativeGUI.msgCustom.dictStrCustomNote.update(OlivaDiceShouHun.msgCustom.dictStrCustomNote)