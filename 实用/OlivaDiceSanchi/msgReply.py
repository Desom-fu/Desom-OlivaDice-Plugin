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
import OlivaDiceSanchi
import OlivaDiceCore

import hashlib
import time
import traceback
from functools import wraps
import copy

def unity_init(plugin_event, Proc):
    pass

def data_init(plugin_event, Proc):
    OlivaDiceSanchi.msgCustomManager.initMsgCustom(Proc.Proc_data['bot_info_dict'])

def unity_reply(plugin_event, Proc):
    OlivaDiceCore.userConfig.setMsgCount()
    dictTValue = OlivaDiceCore.msgCustom.dictTValue.copy()
    dictTValue['tUserName'] = plugin_event.data.sender['name']
    dictTValue['tName'] = plugin_event.data.sender['name']
    dictStrCustom = OlivaDiceCore.msgCustom.dictStrCustomDict[plugin_event.bot_info.hash]
    dictGValue = OlivaDiceCore.msgCustom.dictGValue
    dictTValue.update(dictGValue)
    dictTValue = OlivaDiceCore.msgCustomManager.dictTValueInit(plugin_event, dictTValue)

    valDict = {}
    valDict['dictTValue'] = dictTValue
    valDict['dictStrCustom'] = dictStrCustom
    valDict['tmp_platform'] = plugin_event.platform['platform']

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
    tmp_reast_str = OlivaDiceCore.msgReply.to_half_width(tmp_reast_str)
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
        tmp_hostID = None
        tmp_hagID = None
        tmp_userID = plugin_event.data.user_id
        valDict['tmp_userID'] = tmp_userID
        tmp_list_hit = []
        flag_is_from_master = OlivaDiceCore.ordinaryInviteManager.isInMasterList(
            plugin_event.bot_info.hash,
            OlivaDiceCore.userConfig.getUserHash(
                plugin_event.data.user_id,
                'user',
                plugin_event.platform['platform']
            )
        )
        valDict['flag_is_from_master'] = flag_is_from_master
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
        if isMatchWordStart(tmp_reast_str, 'tq', isCommand = True):
            is_at, at_user_id, tmp_reast_str = OlivaDiceCore.msgReply.parse_at_user(plugin_event, tmp_reast_str, valDict, flag_is_from_group_admin)
            if is_at and not at_user_id:
                return
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'tq')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            # 默认tName是人物卡名
            tmp_pc_id = at_user_id if at_user_id else plugin_event.data.user_id
            tmp_pc_platform = plugin_event.platform['platform']
            tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(
                tmp_pc_id,
                tmp_pc_platform
            )
            tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(
                tmp_pcHash,
                tmp_hagID
            )
            if tmp_pc_name != None:
                dictTValue['tName'] = tmp_pc_name
            else:
                res = plugin_event.get_stranger_info(user_id = tmp_pc_id)
                if res != None:
                    dictTValue['tName'] = res['data']['name']
                else:
                    dictTValue['tName'] = f'用户{tmp_pc_id}'
            flag_hide = False
            if isMatchWordStart(tmp_reast_str, 'h'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'h')
                flag_hide = True
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            # 新增：支持.tq3#3格式
            tq_number = 1
            tq_times = 1
            if tmp_reast_str:
                if '#' in tmp_reast_str:
                    parts = tmp_reast_str.split('#', 1)
                    if parts[0].isdigit():
                        tq_times = int(parts[0])
                        if tq_times > 10:
                            tq_times = 10
                    if parts[1].isdigit():
                        tq_number = int(parts[1])
                else:
                    if tmp_reast_str.isdigit():
                        tq_number = int(tmp_reast_str)
            # 校验铜钱数
            if tq_number < 1 or tq_number > 100:
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                    dictStrCustom['strTQError'], 
                    dictTValue
                )
                replyMsg(plugin_event, tmp_reply_str)
                return
            # 校验次数
            if tq_times < 1 or tq_times > 10:
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                    dictStrCustom['strTQError'], 
                    dictTValue
                )
                replyMsg(plugin_event, tmp_reply_str)
                return
            # 多次铜钱卦
            if tq_times == 1:
                yin_count = 0
                yang_count = 0
                rd = OlivaDiceCore.onedice.RD(f'{tq_number}d2')
                rd.roll()
                if rd.resError is not None:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                        dictStrCustom['strTQError'], 
                        dictTValue
                    )
                    replyMsg(plugin_event, tmp_reply_str)
                    return
                result = []
                for res in rd.resMetaTuple:
                    if res == 1:
                        result.append('阴')
                        yin_count += 1
                    else:
                        result.append('阳')
                        yang_count += 1
                dictTValue['tNumber'] = str(tq_number)
                dictTValue['tYinNumber'] = str(yin_count)
                dictTValue['tYangNumber'] = str(yang_count)
                dictTValue['tResult'] = '、'.join(result)
                # 根据是否暗骰和代骰选择回复方式
                if is_at:
                    if flag_hide and flag_is_from_group:
                        dictTValue['tGroupId'] = str(plugin_event.data.group_id)
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                            dictStrCustom['strTQHideAtOther'], 
                            dictTValue
                        )
                        replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
                            dictStrCustom['strTQHideShowAtOther'], 
                            dictTValue
                        ))
                        OlivaDiceCore.msgReply.replyMsgPrivateByEvent(plugin_event, tmp_reply_str)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                            dictStrCustom['strTQAtOther'], 
                            dictTValue
                        )
                        replyMsg(plugin_event, tmp_reply_str)
                else:
                    if flag_hide and flag_is_from_group:
                        dictTValue['tGroupId'] = str(plugin_event.data.group_id)
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                            dictStrCustom['strTQHide'], 
                            dictTValue
                        )
                        replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
                            dictStrCustom['strTQHideShow'], 
                            dictTValue
                        ))
                        OlivaDiceCore.msgReply.replyMsgPrivateByEvent(plugin_event, tmp_reply_str)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                            dictStrCustom['strTQResult'], 
                            dictTValue
                        )
                        replyMsg(plugin_event, tmp_reply_str)
                return
            else:
                result_list = []
                all_yin_count = 0
                all_yang_count = 0
                for i in range(tq_times):
                    yin_count = 0
                    yang_count = 0
                    rd = OlivaDiceCore.onedice.RD(f'{tq_number}d2')
                    rd.roll()
                    if rd.resError is not None:
                        result_list.append(f'第{i+1}次：铜钱卦出错')
                        continue
                    result = []
                    for res in rd.resMetaTuple:
                        if res == 1:
                            result.append('阴')
                            yin_count += 1
                            all_yin_count += 1
                        else:
                            result.append('阳')
                            yang_count += 1
                            all_yang_count += 1
                    result_list.append(f'第{i+1}次：' + '、'.join(result) + f'（阴:{yin_count} 阳:{yang_count}）')
                dictTValue['tTime'] = str(tq_times)
                dictTValue['tNumber'] = str(tq_number)
                dictTValue['tYinNumber'] = str(all_yin_count)
                dictTValue['tYangNumber'] = str(all_yang_count)
                dictTValue['tResult'] = '\n'.join(result_list)
                # 根据是否暗骰和代骰选择回复方式
                if is_at:
                    if flag_hide and flag_is_from_group:
                        dictTValue['tGroupId'] = str(plugin_event.data.group_id)
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                            dictStrCustom['strTQHideAtOtherMore'], 
                            dictTValue
                        )
                        replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
                            dictStrCustom['strTQHideShowAtOtherMore'], 
                            dictTValue
                        ))
                        OlivaDiceCore.msgReply.replyMsgPrivateByEvent(plugin_event, tmp_reply_str)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                            dictStrCustom['strTQAtOtherMore'], 
                            dictTValue
                        )
                        replyMsg(plugin_event, tmp_reply_str)
                else:
                    if flag_hide and flag_is_from_group:
                        dictTValue['tGroupId'] = str(plugin_event.data.group_id)
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                            dictStrCustom['strTQHideMore'], 
                            dictTValue
                        )
                        replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(
                            dictStrCustom['strTQHideShowMore'], 
                            dictTValue
                        ))
                        OlivaDiceCore.msgReply.replyMsgPrivateByEvent(plugin_event, tmp_reply_str)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                            dictStrCustom['strTQResultMore'], 
                            dictTValue
                        )
                        replyMsg(plugin_event, tmp_reply_str)
                return