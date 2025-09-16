# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   msgReply.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaDiceCore

import hashlib
import time
import traceback
import json
import os
from functools import wraps
import copy

def get_luck_text(luck_num, luck_dict):
    # 默认运势文本
    luck_text = "不可能有这条消息，你升桂了！"
    # 查找匹配的运势文本
    for key, value in luck_dict.items():
        if isinstance(key, tuple):  # 处理范围键
            if key[0] <= luck_num <= key[1]:
                luck_text = value
                break
        elif luck_num == key:  # 处理单个值键
            luck_text = value
            break
    
    return luck_text

def unity_init(plugin_event, Proc):
    pass

def data_init(plugin_event, Proc):
    # 初始化运势文本json文件
    jrrp_text_path = os.path.join('plugin', 'data', 'jrrpChange')
    if not os.path.exists(jrrp_text_path):
        os.makedirs(jrrp_text_path)
    
    json_path = os.path.join(jrrp_text_path, 'luck_text.json')
    
    # 默认运势字典
    default_luck_dict = {
        "1": "哇哦，大成功诶！但是这不是coc，祝你好运！",
        "2-10": "三军听令，自刎刎归天！",
        "11-15": "质疑。唉我真的是服了，天天今日人品这么差劲。",
        "16": "抽的好！奖励你去到处都是果冻的塔进行劲爆路线解密！",
        "17-30": "质疑。唉我真的是服了，天天今日人品这么差劲。",
        "31-50": "O-O 小芙能有什么坏心眼呢？",
        "51-65": "超过一半了，或许今天运气还不错？",
        "66": "抽的好！奖励你蹲着跑去LXVI和一堆圆刺激情碰撞！",
        "67-70": "超过一半了，或许今天的运气还不错？",
        "71-73": "没准今天你能出个金草莓或者过一个榜图？",
        "74": "抽的好！奖励你跑到全是咖啡跳的无名旅馆和冰球斗智斗勇！",
        "75-90": "没准今天你能出个金草莓或者过一个榜图？",
        "91-99": "快去抽卡吧，奇想盲盒和600草莓在等着你！",
        "100": "哇哦，100诶！那你一定能一把理论测试如果Y PP毕加索 秒杀大屠杀 AP+脆肚！"
    }
    
    # 如果json文件不存在，则创建并写入默认值
    if not os.path.exists(json_path):
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(default_luck_dict, f, ensure_ascii=False, indent=4)

def load_luck_dict():
    json_path = os.path.join('plugin', 'data', 'jrrpChange', 'luck_text.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            raw_luck_dict = json.load(f)
        # 转换键格式为代码可用的形式
        luck_dict = {}
        for key, value in raw_luck_dict.items():
            if '-' in key:
                start, end = map(int, key.split('-'))
                luck_dict[(start, end)] = value
            else:
                luck_dict[int(key)] = value
                
        return luck_dict
    except:
        return {}

def poke_jrrp(plugin_event, Proc):
    jrrp_mode = OlivaDiceCore.console.getConsoleSwitchByHash(
        'differentJrrpMode',
        plugin_event.bot_info.hash
    )
    replyMsg = OlivaDiceCore.msgReply.replyMsg
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictTValue['tName'] = '你'
    tmp_pcName = None
    tmp_plName = None
    dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustomDict[plugin_event.bot_info.hash]
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)
    dictTValue = OlivaDiceCore.msgCustomManager.dictTValueInit(plugin_event, dictTValue)
    tmp_pc_id = plugin_event.data.user_id
    if plugin_event.data.target_id != plugin_event.base_info['self_id']:
        return
    tmp_pc_platform = plugin_event.platform['platform']
    if tmp_pcName == None:
        tmp_userHash = OlivaDiceCore.userConfig.getUserHash(
            userId = tmp_pc_id,
            userType = 'user',
            platform = tmp_pc_platform
        )
        tmp_userId = OlivaDiceCore.userConfig.getUserDataByKeyWithHash(
            userHash = tmp_userHash,
            userDataKey = 'userId',
            botHash = plugin_event.bot_info.hash
        )
        if tmp_userId != None:
            tmp_pcName = OlivaDiceCore.userConfig.getUserConfigByKeyWithHash(
                userHash = tmp_userHash,
                userConfigKey = 'userName',
                botHash = plugin_event.bot_info.hash
            )
    res = plugin_event.get_stranger_info(user_id = plugin_event.data.user_id)
    if res != None:
        if tmp_pcName == None:
            tmp_pcName = res['data']['name']
        tmp_plName = res['data']['name']
    dictTValue['tUserName'] = tmp_plName if tmp_plName else tmp_pc_id
    if tmp_pcName != None:
        dictTValue['tName'] = tmp_pcName
        hash_tmp = hashlib.new('md5')
        hash_tmp.update(str(time.strftime('%Y-%m-%d', time.localtime())).encode(encoding='UTF-8'))
        hash_tmp.update(str(plugin_event.data.user_id).encode(encoding='UTF-8'))
        if jrrp_mode == 1:
            hash_tmp.update(str(plugin_event.bot_info.hash).encode(encoding='UTF-8'))
        tmp_jrrp_int = int(int(hash_tmp.hexdigest(), 16) % 100) + 1
        luck_dict = load_luck_dict()
        tmp_jrrp_reply = get_luck_text(int(tmp_jrrp_int), luck_dict)
        dictTValue['tJrrpResult'] = str(tmp_jrrp_int)
        dictTValue['tJrrpText'] = tmp_jrrp_reply
        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strJoyJrrp'], dictTValue)
        replyMsg(plugin_event, tmp_reply_str)

def unity_reply(plugin_event, Proc):
    OlivaDiceCore.userConfig.setMsgCount()
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictTValue['tUserName'] = plugin_event.data.sender['name']
    dictTValue['tName'] = plugin_event.data.sender['name']
    dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustomDict[plugin_event.bot_info.hash]
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)
    dictTValue = OlivaDiceCore.msgCustomManager.dictTValueInit(plugin_event, dictTValue)

    replyMsg = OlivaDiceCore.msgReply.replyMsg
    isMatchWordStart = OlivaDiceCore.msgReply.isMatchWordStart
    getMatchWordStartRight = OlivaDiceCore.msgReply.getMatchWordStartRight
    skipSpaceStart = OlivaDiceCore.msgReply.skipSpaceStart
    skipToRight = OlivaDiceCore.msgReply.skipToRight
    msgIsCommand = OlivaDiceCore.msgReply.msgIsCommand

    tmp_at_str = OlivOS.messageAPI.PARA.at(plugin_event.base_info['self_id']).CQ()
    tmp_at_str_sub = None
    if 'sub_self_id' in plugin_event.data.extend:
        if plugin_event.data.extend['sub_self_id'] != None:
            tmp_at_str_sub = OlivOS.messageAPI.PARA.at(plugin_event.data.extend['sub_self_id']).CQ()
    tmp_command_str_1 = '.'
    tmp_command_str_2 = '。'
    tmp_command_str_3 = '/'
    tmp_reast_str = plugin_event.data.message
    flag_force_reply = False
    flag_is_command = False
    flag_is_from_host = False
    flag_is_from_group = False
    flag_is_from_group_admin = False
    flag_is_from_group_have_admin = False
    flag_is_from_master = False
    if isMatchWordStart(tmp_reast_str, '[CQ:reply,id='):
        tmp_reast_str = skipToRight(tmp_reast_str, ']')
        tmp_reast_str = tmp_reast_str[1:]
        if isMatchWordStart(tmp_reast_str, tmp_at_str):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, tmp_at_str)
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            flag_force_reply = True
    if isMatchWordStart(tmp_reast_str, tmp_at_str):
        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, tmp_at_str)
        tmp_reast_str = skipSpaceStart(tmp_reast_str)
        flag_force_reply = True
    if tmp_at_str_sub != None:
        if isMatchWordStart(tmp_reast_str, tmp_at_str_sub):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, tmp_at_str_sub)
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            flag_force_reply = True
    [tmp_reast_str, flag_is_command] = msgIsCommand(
        tmp_reast_str,
        OlivaDiceCore.crossHook.dictHookList['prefix']
    )
    if flag_is_command:
        tmp_hagID = None
        if plugin_event.plugin_info['func_type'] == 'group_message':
            if plugin_event.data.host_id != None:
                flag_is_from_host = True
            flag_is_from_group = True
        elif plugin_event.plugin_info['func_type'] == 'private_message':
            flag_is_from_group = False
        if flag_is_from_group:
            if 'role' in plugin_event.data.sender:
                flag_is_from_group_have_admin = True
                if plugin_event.data.sender['role'] in ['owner', 'admin']:
                    flag_is_from_group_admin = True
                elif plugin_event.data.sender['role'] in ['sub_admin']:
                    flag_is_from_group_admin = True
                    flag_is_from_group_sub_admin = True
        if flag_is_from_host and flag_is_from_group:
            tmp_hagID = '%s|%s' % (str(plugin_event.data.host_id), str(plugin_event.data.group_id))
        elif flag_is_from_group:
            tmp_hagID = str(plugin_event.data.group_id)
        flag_hostEnable = True
        if flag_is_from_host:
            flag_hostEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = plugin_event.data.host_id,
                userType = 'host',
                platform = plugin_event.platform['platform'],
                userConfigKey = 'hostEnable',
                botHash = plugin_event.bot_info.hash
            )
        flag_hostLocalEnable = True
        if flag_is_from_host:
            flag_hostLocalEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = plugin_event.data.host_id,
                userType = 'host',
                platform = plugin_event.platform['platform'],
                userConfigKey = 'hostLocalEnable',
                botHash = plugin_event.bot_info.hash
            )
        flag_groupEnable = True
        if flag_is_from_group:
            if flag_is_from_host:
                if flag_hostEnable:
                    flag_groupEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                        userId = tmp_hagID,
                        userType = 'group',
                        platform = plugin_event.platform['platform'],
                        userConfigKey = 'groupEnable',
                        botHash = plugin_event.bot_info.hash
                    )
                else:
                    flag_groupEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                        userId = tmp_hagID,
                        userType = 'group',
                        platform = plugin_event.platform['platform'],
                        userConfigKey = 'groupWithHostEnable',
                        botHash = plugin_event.bot_info.hash
                    )
            else:
                flag_groupEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userId = tmp_hagID,
                    userType = 'group',
                    platform = plugin_event.platform['platform'],
                    userConfigKey = 'groupEnable',
                    botHash = plugin_event.bot_info.hash
                )
        #此频道关闭时中断处理
        if not flag_hostLocalEnable and not flag_force_reply:
            return
        #此群关闭时中断处理
        if not flag_groupEnable and not flag_force_reply:
            return
        jrrp_mode = OlivaDiceCore.console.getConsoleSwitchByHash(
            'differentJrrpMode',
            plugin_event.bot_info.hash
        )
        if isMatchWordStart(tmp_reast_str, 'jrrp', isCommand = True):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'jrrp')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_reast_str = tmp_reast_str.rstrip(' ')
            tmp_reply_str = None
            hash_tmp = hashlib.new('md5')
            hash_tmp.update(str(time.strftime('%Y-%m-%d', time.localtime())).encode(encoding='UTF-8'))
            hash_tmp.update(str(plugin_event.data.user_id).encode(encoding='UTF-8'))
            if jrrp_mode == 1:
                hash_tmp.update(str(plugin_event.bot_info.hash).encode(encoding='UTF-8'))
            tmp_jrrp_int = int(int(hash_tmp.hexdigest(), 16) % 100) + 1
            luck_dict = load_luck_dict()
            tmp_jrrp_reply = get_luck_text(int(tmp_jrrp_int), luck_dict)
            dictTValue['tJrrpResult'] = str(tmp_jrrp_int)
            dictTValue['tJrrpText'] = tmp_jrrp_reply
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strJoyJrrp'], dictTValue)
            if tmp_reply_str != None:
                replyMsg(plugin_event, tmp_reply_str)
                plugin_event.set_block()
            return
        elif isMatchWordStart(tmp_reast_str, 'zrrp', isCommand = True):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'zrrp')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_reast_str = tmp_reast_str.rstrip(' ')
            tmp_reply_str = None
            hash_tmp = hashlib.new('md5')
            hash_tmp.update(str(time.strftime('%Y-%m-%d', time.localtime(int(time.mktime(time.localtime())) - 24 * 60 * 60))).encode(encoding='UTF-8'))
            hash_tmp.update(str(plugin_event.data.user_id).encode(encoding='UTF-8'))
            if jrrp_mode == 1:
                hash_tmp.update(str(plugin_event.bot_info.hash).encode(encoding='UTF-8'))
            tmp_jrrp_int = int(int(hash_tmp.hexdigest(), 16) % 100) + 1
            luck_dict = load_luck_dict()
            tmp_jrrp_reply = get_luck_text(int(tmp_jrrp_int), luck_dict)
            dictTValue['tJrrpResult'] = str(tmp_jrrp_int)
            dictTValue['tJrrpText'] = tmp_jrrp_reply
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strJoyZrrp'], dictTValue)
            if tmp_reply_str != None:
                replyMsg(plugin_event, tmp_reply_str)
                plugin_event.set_block()
            return
        elif isMatchWordStart(tmp_reast_str, 'mrrp', isCommand = True):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'mrrp')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_reast_str = tmp_reast_str.rstrip(' ')
            tmp_reply_str = None
            hash_tmp = hashlib.new('md5')
            hash_tmp.update(str(time.strftime('%Y-%m-%d', time.localtime(int(time.mktime(time.localtime())) + 24 * 60 * 60))).encode(encoding='UTF-8'))
            hash_tmp.update(str(plugin_event.data.user_id).encode(encoding='UTF-8'))
            if jrrp_mode == 1:
                hash_tmp.update(str(plugin_event.bot_info.hash).encode(encoding='UTF-8'))
            tmp_jrrp_int = int(int(hash_tmp.hexdigest(), 16) % 100) + 1
            luck_dict = load_luck_dict()
            tmp_jrrp_reply = get_luck_text(int(tmp_jrrp_int), luck_dict)
            dictTValue['tJrrpResult'] = str(tmp_jrrp_int)
            dictTValue['tJrrpText'] = tmp_jrrp_reply
            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strJoyMrrp'], dictTValue)
            if tmp_reply_str != None:
                replyMsg(plugin_event, tmp_reply_str)
                plugin_event.set_block()
            return