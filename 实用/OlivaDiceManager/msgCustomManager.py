# -*- encoding: utf-8 -*-
'''
自定义回复管理器
'''

import OlivOS
import OlivaDiceCore
import OlivaDiceManager
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
        for dictStrCustom_this in OlivaDiceManager.msgCustom.dictStrCustom:
            if dictStrCustom_this not in OlivaDiceCore.msgCustom.dictStrCustomDict[bot_info_dict_this]:
                OlivaDiceCore.msgCustom.dictStrCustomDict[bot_info_dict_this][dictStrCustom_this] = OlivaDiceManager.msgCustom.dictStrCustom[dictStrCustom_this]
        for dictHelpDoc_this in OlivaDiceManager.msgCustom.dictHelpDocTemp:
            if dictHelpDoc_this not in OlivaDiceCore.helpDocData.dictHelpDoc[bot_info_dict_this]:
                OlivaDiceCore.helpDocData.dictHelpDoc[bot_info_dict_this][dictHelpDoc_this] = OlivaDiceManager.msgCustom.dictHelpDocTemp[dictHelpDoc_this]
        if has_NativeGUI:
            for dictStrCustomNote_this in OlivaDiceManager.msgCustom.dictStrCustomNote:
                if dictStrCustomNote_this not in OlivaDiceNativeGUI.msgCustom.dictStrCustomNote:
                    OlivaDiceNativeGUI.msgCustom.dictStrCustomNote[dictStrCustomNote_this] = OlivaDiceManager.msgCustom.dictStrCustomNote[dictStrCustomNote_this]   
    OlivaDiceCore.msgCustom.dictStrConst.update(OlivaDiceManager.msgCustom.dictStrConst)
    OlivaDiceCore.msgCustom.dictGValue.update(OlivaDiceManager.msgCustom.dictGValue)
    OlivaDiceCore.msgCustom.dictTValue.update(OlivaDiceManager.msgCustom.dictTValue)
    if has_NativeGUI:
        OlivaDiceNativeGUI.msgCustom.dictStrCustomNote.update(OlivaDiceManager.msgCustom.dictStrCustomNote)
