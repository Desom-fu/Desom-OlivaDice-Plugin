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
import re
import random

def replace_skills(expr_str, skill_valueTable, tmp_pcCardRule):
    """
    使用 getExpression 函数替换技能名，并将 0dX 替换为 0
    """
    if not expr_str:
        return expr_str, expr_str
    # 使用 getExpression 处理表达式
    [processed_expr, expr_show] = OlivaDiceCore.msgReply.getExpression(
        data=expr_str,
        reverse=False,
        valueTable=skill_valueTable,
        pcCardRule=tmp_pcCardRule,
        flagDynamic=True,
        ruleMode='default'
    )
    [processed_detail, expr_show_2] = OlivaDiceCore.msgReply.getExpression(
        data=expr_str,
        reverse=False,
        valueTable=skill_valueTable,
        pcCardRule=tmp_pcCardRule,
        flagDynamic=False,
        ruleMode='default'
    )
    if expr_show != expr_show_2:
        processed_detail = processed_expr
    replaced_expr = processed_expr
    replaced_detail = processed_detail
    # 处理 getExpression 的特殊格式（如 {技能名}）
    if '{' in replaced_detail and '}' in replaced_detail:
        # 提取所有变量
        vars = re.findall(r'\{([^}]+)\}', replaced_detail)
        for var in vars:
            if var in skill_valueTable:
                # 替换为技能名(值)格式
                replaced_detail = replaced_detail.replace(
                    f'{{{var}}}',
                    f'{var}({skill_valueTable[var]})'
                )
    # 替换 0dX 为 0
    replaced_expr = re.sub(r'(?:\b0|\(0\))[dD]\d+\b', '0', replaced_expr)
    return replaced_expr, replaced_detail

def parse_bp_parameters(expr_str):
    """
    解析表达式中的b/p参数
    返回: cleaned_expr, b_count, p_count
    """
    isMatchWordStart = OlivaDiceCore.msgReply.isMatchWordStart
    getMatchWordStartRight = OlivaDiceCore.msgReply.getMatchWordStartRight
    skipSpaceStart = OlivaDiceCore.msgReply.skipSpaceStart
    
    b_count = 0  # b参数（阴转阳）
    p_count = 0  # p参数（阳转阴+铜钱）
    tmp_reast_str = expr_str
    
    # 循环处理所有参数
    while tmp_reast_str:
        original_str = tmp_reast_str
        
        # 处理b参数（阴转阳）
        if isMatchWordStart(tmp_reast_str, 'b'):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'b')
            # 检查是否有数字指定，只取一位
            if len(tmp_reast_str) > 0 and tmp_reast_str[0].isdigit():
                b_count += int(tmp_reast_str[0])
                tmp_reast_str = tmp_reast_str[1:]
            else:
                b_count += 1  # 默认为1
            # 移除可能的+号
            if len(tmp_reast_str) > 0 and tmp_reast_str[0] == '+':
                tmp_reast_str = tmp_reast_str[1:]
            continue
        
        # 处理p参数（阳转阴+铜钱）
        elif isMatchWordStart(tmp_reast_str, 'p'):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'p')
            # 检查是否有数字指定，只取一位
            if len(tmp_reast_str) > 0 and tmp_reast_str[0].isdigit():
                p_count += int(tmp_reast_str[0])
                tmp_reast_str = tmp_reast_str[1:]
            else:
                p_count += 1  # 默认为1
            # 移除可能的+号
            if len(tmp_reast_str) > 0 and tmp_reast_str[0] == '+':
                tmp_reast_str = tmp_reast_str[1:]
            continue
        
        # 如果没有匹配到任何参数，跳出循环
        if tmp_reast_str == original_str:
            break
    
    # 跳过空格并返回清理后的表达式
    cleaned_expr = skipSpaceStart(tmp_reast_str)
    
    return cleaned_expr, b_count, p_count

def apply_bp_transformations(results, b_count, p_count):
    """
    应用b/p转换到铜钱卦结果
    b_count: 阴转阳的数量
    p_count: 阳转阴的数量（同时增加劣势铜钱数）
    返回: (转换后的结果列表, 转换说明列表, 额外增加的铜钱数)
    
    劣势规则：每个p转换会增加一枚标记为(劣势)的铜钱，且劣势铜钱投出的阳也可以被继续转换
    """
    if b_count <= 0 and p_count <= 0:
        return results, [], 0
    
    # 复制结果以避免修改原数组
    new_results = results.copy()
    transformations = []
    extra_coins = 0
    
    # 执行b转换（阴转阳）
    yin_indices = [i for i, r in enumerate(new_results) if r.startswith('阴')]
    actual_b = min(b_count, len(yin_indices))
    if actual_b > 0:
        # 随机选择要转换的阴
        selected_yin = random.sample(yin_indices, actual_b)
        for idx in selected_yin:
            new_results[idx] = '阳(阴)'
            transformations.append(f"位置{idx+1}: 阴→阳")
    
    # 执行p转换（阳转阴+劣势铜钱）
    # 需要考虑劣势可以叠加，所以要循环处理每个p转换
    remaining_p = p_count
    while remaining_p > 0:
        # 获取当前所有阳的位置（包括新增加的劣势阳）
        yang_indices = [i for i, r in enumerate(new_results) if r.startswith('阳')]
        
        if len(yang_indices) == 0:
            # 没有阳可以转换了，退出循环
            break
        
        # 每次只转换一个阳（劣势的定义是每个劣势转换一个阳）
        actual_p = min(1, len(yang_indices))
        if actual_p > 0:
            # 随机选择要转换的阳
            selected_yang = random.sample(yang_indices, actual_p)
            for idx in selected_yang:
                old_value = new_results[idx]
                # 保留原有的劣势标记
                if '(劣势)' in old_value:
                    new_results[idx] = '阴(阳)(劣势)'
                else:
                    new_results[idx] = '阴(阳)'
                transformations.append(f"位置{idx+1}: 阳→阴")
            
            # 增加一枚劣势铜钱
            extra_coins += 1
            coin_result = random.choice(['阴', '阳'])
            coin_result += '(劣势)'  # 所有劣势铜钱都标记为劣势
            new_results.append(coin_result)
        
        remaining_p -= actual_p
    
    return new_results, transformations, extra_coins

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
            # 获取人物卡规则
            tmp_pcCardRule = 'default'
            tmp_pcCardRule_new = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(tmp_pcHash, tmp_pc_name)
            if tmp_pcCardRule_new != None:
                tmp_pcCardRule = tmp_pcCardRule_new
            if tmp_pc_name != None:
                dictTValue['tName'] = tmp_pc_name
            else:
                res = plugin_event.get_stranger_info(user_id = tmp_pc_id)
                if res != None:
                    dictTValue['tName'] = res['data']['name']
                else:
                    dictTValue['tName'] = f'用户{tmp_pc_id}'
            # 获取技能数据
            pc_skills = OlivaDiceCore.pcCard.pcCardDataGetByPcName(tmp_pcHash, hagId=tmp_hagID) if tmp_pc_name else {}
            skill_valueTable = pc_skills.copy()
            if tmp_pc_name != None:
                skill_valueTable.update(
                    OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                        pcHash = tmp_pcHash,
                        pcCardName = tmp_pc_name,
                        dataKey = 'mappingRecord',
                        resDefault = {}
                    )
                )
            
            # 1. 首先解析h参数（暗骰）
            flag_hide = False
            if isMatchWordStart(tmp_reast_str, 'h'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'h')
                flag_hide = True
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            
            # 2. 解析次数#铜钱数格式和b/p参数
            tq_number = 3  # 默认3
            tq_times = 1
            expr_show = None
            b_count = 0
            p_count = 0
            
            if tmp_reast_str:
                if '#' in tmp_reast_str:
                    parts = tmp_reast_str.split('#', 1)
                    front_part = parts[0].strip()
                    back_part = parts[1].strip()
                    
                    # 处理前半部分（次数）
                    if front_part:
                        if front_part.isdigit():
                            tq_times = int(front_part)
                        else:
                            # 前半部分是表达式，按1次处理
                            tq_times = 1
                    
                    # 在后半部分解析b/p参数
                    back_part, b_count, p_count = parse_bp_parameters(back_part)
                    
                    # 处理后半部分剩余的（铜钱数）
                    if back_part:
                        if back_part.isdigit():
                            tq_number = int(back_part)
                        else:
                            # 后半部分是表达式，需要解析
                            try:
                                processed_expr, expr_show = replace_skills(back_part, skill_valueTable, tmp_pcCardRule)
                                rd = OlivaDiceCore.onedice.RD(processed_expr)
                                rd.roll()
                                if rd.resError is None:
                                    tq_number = max(1, min(100, int(rd.resInt)))
                                    # 构建详细显示过程
                                    if rd.resDetail and rd.resDetail != str(rd.resInt):
                                        if expr_show == rd.resDetail:
                                            expr_show = f"{expr_show}={tq_number}"
                                        else:
                                            expr_show = f"{expr_show}={rd.resDetail}={tq_number}"
                                    else:
                                        if expr_show != str(tq_number):
                                            expr_show = f"{expr_show}={tq_number}"
                                        else:
                                            expr_show = str(tq_number)
                                else:
                                    raise ValueError("表达式解析错误")
                            except:
                                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                                    dictStrCustom['strTQError'], 
                                    dictTValue
                                )
                                replyMsg(plugin_event, tmp_reply_str)
                                return
                else:
                    # 没有#号的情况，在整个字符串中解析b/p参数
                    tmp_reast_str, b_count, p_count = parse_bp_parameters(tmp_reast_str)
                    
                    if tmp_reast_str:
                        if tmp_reast_str.isdigit():
                            tq_number = int(tmp_reast_str)
                        else:
                            # 是表达式，需要解析
                            try:
                                processed_expr, expr_show = replace_skills(tmp_reast_str, skill_valueTable, tmp_pcCardRule)
                                rd = OlivaDiceCore.onedice.RD(processed_expr)
                                rd.roll()
                                if rd.resError is None:
                                    tq_number = max(1, min(100, int(rd.resInt)))
                                    # 构建详细显示过程
                                    if rd.resDetail and rd.resDetail != str(rd.resInt):
                                        if expr_show == rd.resDetail:
                                            expr_show = f"{expr_show}={tq_number}"
                                        else:
                                            expr_show = f"{expr_show}={rd.resDetail}={tq_number}"
                                    else:
                                        if expr_show != str(tq_number):
                                            expr_show = f"{expr_show}={tq_number}"
                                        else:
                                            expr_show = str(tq_number)
                                else:
                                    raise ValueError("表达式解析错误")
                            except:
                                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(
                                    dictStrCustom['strTQError'], 
                                    dictTValue
                                )
                                replyMsg(plugin_event, tmp_reply_str)
                                return
            
            # 限制次数
            if tq_times > 10:
                tq_times = 10
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
                # 基础投掷结果
                result = []
                for res in rd.resMetaTuple:
                    if res == 1:
                        result.append('阴')
                        yin_count += 1
                    else:
                        result.append('阳')
                        yang_count += 1
                
                # 应用b/p转换
                result, transformations, extra_coins = apply_bp_transformations(result, b_count, p_count)
                
                # 重新计算阴阳数量
                final_yin_count = 0
                final_yang_count = 0
                for res in result:
                    if res.startswith('阴'):
                        final_yin_count += 1
                    elif res.startswith('阳'):
                        final_yang_count += 1
                
                # 设置显示参数
                dictTValue['tNumber'] = str(tq_number + extra_coins)
                dictTValue['tOriginalNumber'] = str(tq_number)
                dictTValue['tYinNumber'] = str(final_yin_count)
                dictTValue['tYangNumber'] = str(final_yang_count)
                dictTValue['tResult'] = '、'.join(result)
                
                # 设置表达式显示
                if expr_show:
                    dictTValue['tExprShow'] = f'（{expr_show}）'
                else:
                    dictTValue['tExprShow'] = ''
                
                # 设置额外铜钱显示
                if extra_coins > 0:
                    dictTValue['tExtraCoinsText'] = f'，劣势转换增加{extra_coins}枚'
                else:
                    dictTValue['tExtraCoinsText'] = ''
                
                # 设置转换过程显示
                transform_info = []
                if b_count > 0:
                    transform_info.append(f'优势{b_count}')
                if p_count > 0:
                    transform_info.append(f'劣势{p_count}')
                if transform_info:
                    dictTValue['tTransformText'] = f'（{"/".join(transform_info)}转换）'
                else:
                    dictTValue['tTransformText'] = ''
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
                all_extra_coins = 0
                for i in range(tq_times):
                    yin_count = 0
                    yang_count = 0
                    rd = OlivaDiceCore.onedice.RD(f'{tq_number}d2')
                    rd.roll()
                    if rd.resError is not None:
                        result_list.append(f'第{i+1}次：铜钱卦出错')
                        continue
                    # 基础投掷结果
                    result = []
                    for res in rd.resMetaTuple:
                        if res == 1:
                            result.append('阴')
                            yin_count += 1
                        else:
                            result.append('阳')
                            yang_count += 1
                    
                    # 应用b/p转换
                    result, transformations, extra_coins = apply_bp_transformations(result, b_count, p_count)
                    all_extra_coins += extra_coins
                    
                    # 重新计算阴阳数量
                    final_yin_count = 0
                    final_yang_count = 0
                    for res in result:
                        if res.startswith('阴'):
                            final_yin_count += 1
                            all_yin_count += 1
                        elif res.startswith('阳'):
                            final_yang_count += 1
                            all_yang_count += 1
                    
                    # 构建结果字符串
                    result_str = f'第{i+1}次：' + '、'.join(result) + f'（阴:{final_yin_count} 阳:{final_yang_count}）'
                    if transformations:
                        result_str += f' [{", ".join(transformations)}]'
                    result_list.append(result_str)
                
                dictTValue['tTime'] = str(tq_times)
                dictTValue['tNumber'] = str(tq_number + all_extra_coins)
                dictTValue['tOriginalNumber'] = str(tq_number)
                dictTValue['tYinNumber'] = str(all_yin_count)
                dictTValue['tYangNumber'] = str(all_yang_count)
                dictTValue['tResult'] = '\n'.join(result_list)
                
                # 设置表达式显示
                if expr_show:
                    dictTValue['tExprShow'] = f'（{expr_show}）'
                else:
                    dictTValue['tExprShow'] = ''
                
                # 设置所有额外铜钱显示
                if all_extra_coins > 0:
                    dictTValue['tAllExtraCoinsText'] = f'，劣势转换总共增加{all_extra_coins}枚'
                else:
                    dictTValue['tAllExtraCoinsText'] = ''
                
                # 设置b/p参数显示
                bp_info = []
                if b_count > 0:
                    bp_info.append(f'优势{b_count}')
                if p_count > 0:
                    bp_info.append(f'劣势{p_count}')
                if bp_info:
                    dictTValue['tBPText'] = f'（每次{"/".join(bp_info)}转换）'
                else:
                    dictTValue['tBPText'] = ''
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