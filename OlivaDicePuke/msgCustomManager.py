# -*- encoding: utf-8 -*-
'''
@File      :   msgCustomManager.py
@Author    :   Desom-fu
@Contact   :   Desom233@outlook.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaDiceCore
import OlivaDicePuke
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
        for dictStrCustom_this in OlivaDicePuke.msgCustom.dictStrCustom:
            if dictStrCustom_this not in OlivaDiceCore.msgCustom.dictStrCustomDict[bot_info_dict_this]:
                OlivaDiceCore.msgCustom.dictStrCustomDict[bot_info_dict_this][dictStrCustom_this] = OlivaDicePuke.msgCustom.dictStrCustom[dictStrCustom_this]
        for dictHelpDoc_this in OlivaDicePuke.msgCustom.dictHelpDocTemp:
            if dictHelpDoc_this not in OlivaDiceCore.helpDocData.dictHelpDoc[bot_info_dict_this]:
                OlivaDiceCore.helpDocData.dictHelpDoc[bot_info_dict_this][dictHelpDoc_this] = OlivaDicePuke.msgCustom.dictHelpDocTemp[dictHelpDoc_this]
        if has_NativeGUI:
            for dictStrCustomNote_this in OlivaDicePuke.msgCustom.dictStrCustomNote:
                if dictStrCustomNote_this not in OlivaDiceNativeGUI.msgCustom.dictStrCustomNote:
                    OlivaDiceNativeGUI.msgCustom.dictStrCustomNote[dictStrCustomNote_this] = OlivaDicePuke.msgCustom.dictStrCustomNote[dictStrCustomNote_this]   
    OlivaDiceCore.msgCustom.dictStrConst.update(OlivaDicePuke.msgCustom.dictStrConst)
    OlivaDiceCore.msgCustom.dictGValue.update(OlivaDicePuke.msgCustom.dictGValue)
    OlivaDiceCore.msgCustom.dictTValue.update(OlivaDicePuke.msgCustom.dictTValue)
    if has_NativeGUI:
        OlivaDiceNativeGUI.msgCustom.dictStrCustomNote.update(OlivaDicePuke.msgCustom.dictStrCustomNote)
