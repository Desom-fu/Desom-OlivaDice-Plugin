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

import hashlib
import time
import traceback
import re
from functools import wraps
import copy

def unity_init(plugin_event, Proc):
    pass

def data_init(plugin_event, Proc):
    OlivaDiceShouHun.msgCustomManager.initMsgCustom(Proc.Proc_data['bot_info_dict'])

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
    tmp_reast_str = to_half_width(tmp_reast_str)
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
        if isMatchWordStart(tmp_reast_str, 'sh', isCommand = True):
            is_at, at_user_id, tmp_reast_str = OlivaDiceCore.msgReply.parse_at_user(plugin_event, tmp_reast_str, valDict, flag_is_from_group_admin)
            if is_at and not at_user_id:
                return
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'sh')
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
            flag_hide = False
            if isMatchWordStart(tmp_reast_str, 'h'):
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'h')
                flag_hide = True
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            
            # 处理奖励/惩罚等级
            flag_bp_type = 0  # 0无 1奖励 2惩罚
            flag_bp_count = 1
            if isMatchWordStart(tmp_reast_str, 'b'):
                flag_bp_type = 1
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'b')
                # 检查是否有数字指定
                if len(tmp_reast_str) > 0 and tmp_reast_str[0].isdigit():
                    flag_bp_count = int(tmp_reast_str[0])
                    tmp_reast_str = tmp_reast_str[1:]
                # 移除可能的+号
                if len(tmp_reast_str) > 0 and tmp_reast_str[0] == '+':
                    tmp_reast_str = tmp_reast_str[1:]
            elif isMatchWordStart(tmp_reast_str, 'p'):
                flag_bp_type = 2
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'p')
                # 检查是否有数字指定
                if len(tmp_reast_str) > 0 and tmp_reast_str[0].isdigit():
                    flag_bp_count = int(tmp_reast_str[0])
                    tmp_reast_str = tmp_reast_str[1:]
                # 移除可能的+号
                if len(tmp_reast_str) > 0 and tmp_reast_str[0] == '+':
                    tmp_reast_str = tmp_reast_str[1:]
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            
            # 分割前后表达式
            is_number = False
            is_x = False
            parts = tmp_reast_str.split('#')
            front_expr = parts[0].strip() if len(parts) > 0 and parts[0].strip() else None
            front_expr_str = front_expr
            back_expr_str = parts[1].strip() if len(parts) > 1 else '10'
            dice_20 = '1D20' # 默认值 1D20
            if not back_expr_str:
                back_expr_str = '10'
            # 出值解析
            if front_expr:
                # 完全指定点数
                if front_expr.isdigit():
                    is_number = True
                # 指定D20点数
                elif isMatchWordStart(front_expr, 'x'):
                    front_expr = getMatchWordStartRight(front_expr, 'x')
                    front_expr_str = front_expr
                    # 用 + 来分隔
                    if '+' in front_expr:
                        parts_2 = front_expr.split('+', 1)
                        dice_20 = parts_2[0].strip() if parts_2[0].strip() else '1D20'
                        front_expr = parts_2[1].strip() if parts_2[1].strip() else None
                        front_expr_str = front_expr
                        # 限定x后面最多是纯数字
                        if not dice_20.isdigit():
                            dice_20 = '1D20'
                        else:
                            # 最小是0
                            dice_num = int(dice_20)
                            dice_num = max(0, dice_num)
                            dice_20 = str(dice_num)
                            is_x = True
                    else:
                        if front_expr.isdigit():
                            dice_num = int(front_expr)
                            dice_num = max(0, dice_num)
                            dice_20 = str(dice_num)
                            front_expr = None
                            is_x = True
                        else:
                            # 抛出错误
                            front_expr = front_expr_str
                if front_expr:
                    # 1. 只匹配 Xd20+
                    match_xd20_plus = re.match(r'^(\d*)[dD]20\s*\+\s*', front_expr, re.IGNORECASE)
                    if match_xd20_plus:
                        # 处理 X（D20 视为 1D20）
                        x_str = match_xd20_plus.group(1)
                        x = int(x_str) if x_str else 1  # 无数字时默认为1
                        # 有 x 限制就跳过
                        if not is_x:
                            dice_20 = f"{x}D20"
                        # 移除 Xd20+ 部分
                        front_expr = front_expr[len(match_xd20_plus.group(0)):].strip()
                        front_expr_str = front_expr if front_expr else None
                    else:
                        # 2. 如果不是 Xd20+，继续其他逻辑
                        # 匹配纯 Xd20 或 D20
                        match_pure_xd20 = re.match(r'^(\d*)[dD]20\b', front_expr, re.IGNORECASE)
                        if match_pure_xd20:
                            x_str = match_pure_xd20.group(1)
                            x = int(x_str) if x_str else 1  # D20 视为 1D20
                            # 有 x 限制就跳过
                            if not is_x:
                                dice_20 = f"{x}D20"
                            front_expr = front_expr[len(match_pure_xd20.group(0)):].strip()
                            front_expr_str = front_expr if front_expr else None
            # 处理挑战奖励/惩罚等级
            back_flag_bp_type = 0
            back_flag_bp_count = 1
            if back_expr_str:
                if isMatchWordStart(back_expr_str, 'b'):
                    back_flag_bp_type = 1
                    back_expr_str = getMatchWordStartRight(back_expr_str, 'b')
                    # 检查是否有数字指定
                    if len(back_expr_str) > 0 and back_expr_str[0].isdigit():
                        back_flag_bp_count = int(back_expr_str[0])
                        back_expr_str = back_expr_str[1:]
                    # 移除可能的+号
                    if len(back_expr_str) > 0 and back_expr_str[0] == '+':
                        back_expr_str = back_expr_str[1:]
                elif isMatchWordStart(back_expr_str, 'p'):
                    back_flag_bp_type = 2
                    back_expr_str = getMatchWordStartRight(back_expr_str, 'p')
                    # 检查是否有数字指定
                    if len(back_expr_str) > 0 and back_expr_str[0].isdigit():
                        back_flag_bp_count = int(back_expr_str[0])
                        back_expr_str = back_expr_str[1:]
                    # 移除可能的+号
                    if len(back_expr_str) > 0 and back_expr_str[0] == '+':
                        back_expr_str = back_expr_str[1:]
                back_expr_str = skipSpaceStart(back_expr_str)
            
            # 处理挑战值的固定d20
            is_back_x = False
            back_fixed_d20 = 0
            back_fixed_display = ''
            if isMatchWordStart(back_expr_str, 'x'):
                back_expr_str = getMatchWordStartRight(back_expr_str, 'x')
                back_expr_str_temp = back_expr_str
                # 用 + 来分隔
                if '+' in back_expr_str:
                    parts_2 = back_expr_str.split('+', 1)
                    back_dice_str = parts_2[0].strip() if parts_2[0].strip() else None
                    back_expr_str = parts_2[1].strip() if len(parts_2) > 1 and parts_2[1].strip() else ''
                    if back_dice_str and back_dice_str.isdigit():
                        back_fixed_d20 = max(1, int(back_dice_str))
                        is_back_x = True
                    else:
                        # 错误，恢复原状
                        back_expr_str = back_expr_str_temp
                else:
                    if back_expr_str.isdigit():
                        back_fixed_d20 = max(1, int(back_expr_str))
                        is_back_x = True
                        back_expr_str = ''
                    else:
                        # 错误，恢复原状
                        back_expr_str = back_expr_str_temp
                if is_back_x:
                    if 1 <= back_fixed_d20 <= 20:
                        back_fixed_display = f"1D20({back_fixed_d20})"
                    else:
                        back_fixed_display = f"固定值({back_fixed_d20})"
                else:
                    dictTValue['tRollPara'] = back_expr_str_temp
                    dictTValue['tResult'] = "错误的挑战指定点数"
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strShError'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    return
            
            # 获取模板配置
            tmp_template_name = 'default'
            tmp_template_customDefault = None
            if flag_is_from_group:
                tmp_groupTemplate = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userId = tmp_hagID,
                    userType = 'group',
                    platform = plugin_event.platform['platform'],
                    userConfigKey = 'groupTemplate',
                    botHash = plugin_event.bot_info.hash
                )
                if tmp_groupTemplate != None:
                    tmp_template_name = tmp_groupTemplate
            tmp_template = OlivaDiceCore.pcCard.pcCardDataGetTemplateByKey(tmp_template_name)
            if tmp_template != None and 'customDefault' in tmp_template:
                tmp_template_customDefault = tmp_template['customDefault']
            
            # 计算前项 (1D20 + 前项表达式)
            if not is_number:
                # D20 或指定点数
                rd_d20 = OlivaDiceCore.onedice.RD(dice_20, tmp_template_customDefault)
                rd_d20.roll()
                if rd_d20.resError != None:
                    dictTValue['tRollPara'] = front_expr_str
                    error_msg = OlivaDiceCore.msgReplyModel.get_SkillCheckError(rd_d20.resError, dictStrCustom, dictTValue)
                    dictTValue['tResult'] = f"错误的指定点数：{error_msg}"
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strShError'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    return

            if front_expr:
                # 技能替换
                front_expr, front_detail = replace_skills(front_expr.replace('=', '').replace(' ', ''), skill_valueTable, tmp_pcCardRule)
                rd_front = OlivaDiceCore.onedice.RD(front_expr, tmp_template_customDefault)
                rd_front.roll()
                if rd_front.resError != None:
                    dictTValue['tRollPara'] = front_expr_str
                    error_msg = OlivaDiceCore.msgReplyModel.get_SkillCheckError(rd_front.resError, dictStrCustom, dictTValue)
                    dictTValue['tResult'] = f"错误的出值：{error_msg}"
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strShError'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                    return
                if not is_number:
                    front_result = rd_d20.resInt + rd_front.resInt
                    base_front_str = f"{front_detail}={rd_d20.resInt}+{rd_front.resDetail}={front_result}"
                    if not rd_front.resDetail:
                        base_front_str = f"{front_detail}={front_result}"
                        if front_result != rd_d20.resInt:
                            base_front_str = f"{front_detail}={rd_d20.resInt}+{rd_front.resInt}={front_result}"
                    if is_x:
                        front_detail = f"1D20+{base_front_str}" if 1 <= rd_d20.resInt <= 20 else f"固定值({dice_20})+{base_front_str}"
                    else:
                        front_detail = f"{dice_20}+{base_front_str}"
                else:
                    front_result = rd_front.resInt
                    base_front_str = front_detail
                    front_detail = front_detail
            else:
                front_result = rd_d20.resInt
                if is_x:
                    front_detail = f"1D20={front_result}" if 1 <= rd_d20.resInt <= 20 else f"固定值({dice_20})={front_result}"
                else:
                    front_detail = f"{dice_20}={front_result}"

            # 计算后项
            # 处理技能名和表达式
            back_expr, back_detail = replace_skills(back_expr_str.replace('=', '').replace(' ', ''), skill_valueTable, tmp_pcCardRule)
            if not back_expr:
                back_expr = '0' if is_back_x else '10'
            rd_back = OlivaDiceCore.onedice.RD(back_expr, tmp_template_customDefault)
            rd_back.roll()
            
            if rd_back.resError != None:
                dictTValue['tRollPara'] = back_expr_str
                error_msg = OlivaDiceCore.msgReplyModel.get_SkillCheckError(rd_back.resError, dictStrCustom, dictTValue)
                dictTValue['tResult'] = f"错误的挑战值：{error_msg}"
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strShError'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
                return
            
            back_result = rd_back.resInt
            if is_back_x:
                back_result += back_fixed_d20
            # 显示处理
            if rd_back.resDetail and rd_back.resDetail != str(rd_back.resInt):
                if back_detail == rd_back.resDetail:
                    back_detail = f"{back_detail}={back_result - back_fixed_d20 if is_back_x else back_result}"
                else:
                    back_detail = f"{back_detail}={rd_back.resDetail}={back_result - back_fixed_d20 if is_back_x else back_result}"
            else:
                back_detail = back_result - back_fixed_d20 if is_back_x else back_result
            # 挑战值固定D20的显示
            if is_back_x:
                if back_expr != '0':
                    back_detail = f"{back_detail}+({back_fixed_display})={back_result}"
                else:
                    if 1 <= back_fixed_d20 <= 20:
                        back_fixed_display = f"1D20={back_fixed_d20}"
                    else:
                        back_fixed_display = f"固定值({back_fixed_d20})={back_fixed_d20}"
                    back_detail = back_fixed_display

            # 判断结果
            tmpSkillCheckType = OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FAIL
            success_level = 0
            b_bouns = 0
            p_bouns = 0
            b_b_bouns = 0
            b_p_bouns = 0
            front_great_success = 0
            front_great_fail = 0
            back_great_success = 0
            back_great_fail = 0

            # 调用d20计算函数来计算成功等级奖励
            d20_challenge_bonus, back_great_success, back_great_fail, back_d20_time = calculate_d20_success_level(rd_back)
            
            # 固定值的成功等级判断
            if is_back_x:
                if back_fixed_d20 <= 1:
                    d20_challenge_bonus += 1
                    back_great_fail += 1
                elif back_fixed_d20 >= 20:
                    d20_challenge_bonus -= 1
                    back_great_success += 1
                back_d20_time += 1
            
            if front_result > back_result:
                tmpSkillCheckType = OlivaDiceCore.skillCheck.resultType.SKILLCHECK_SUCCESS
                # 计算成功等级
                success_level = max(1, (front_result - back_result + 4) // 5)  # 向上取整
                # 获取初始成功等级
                original_success_level = success_level
                
                # 处理奖励/惩罚等级
                if flag_bp_type == 1:
                    b_bouns = flag_bp_count
                    success_level += b_bouns
                elif flag_bp_type == 2:
                    p_bouns = flag_bp_count
                    success_level -= p_bouns
                # 处理对方奖励/惩罚等级
                if back_flag_bp_type == 1:
                    b_b_bouns = back_flag_bp_count
                    success_level -= b_b_bouns
                elif back_flag_bp_type == 2:
                    b_p_bouns = back_flag_bp_count
                    success_level += b_p_bouns

                if not is_number:
                    # 处理大成功/大失败
                    if rd_d20.resInt >= 20:
                        tmpSkillCheckType = OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_SUCCESS
                        front_great_success = 1
                        success_level += front_great_success
            if not is_number:
                # 大失败要挪出来     
                if rd_d20.resInt == 1:
                    tmpSkillCheckType = OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_FAIL
                    front_great_fail = 1
                    success_level -= front_great_fail
            
            success_level += d20_challenge_bonus
            success_level = max(0, success_level)
            
            # 构建回复
            front_detail = format_long_dice_rolls(front_detail)
            back_detail = format_long_dice_rolls(back_detail)
            dictTValue['tFrontResult'] = front_detail
            dictTValue['tBackResult'] = back_detail
            dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgReplyModel.get_SkillCheckResult(tmpSkillCheckType, dictStrCustom, dictTValue)
            
            # 添加成功等级
            if front_result > back_result:
                if success_level <= 0:
                    if tmpSkillCheckType in [
                        OlivaDiceCore.skillCheck.resultType.SKILLCHECK_SUCCESS, 
                        OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_SUCCESS
                        ]:
                        dictTValue['tSkillCheckReasult'] = '' # 成功等级小于等于0平手，不显示成功文案
                # 构建计算过程字符串
                calc_steps = []
                if front_great_success > 0:
                    calc_steps.append(f"+{front_great_success}(大成功)")
                if front_great_fail > 0:
                    calc_steps.append(f"-{front_great_fail}(大失败)")
                if b_bouns > 0:
                    calc_steps.append(f"+{b_bouns}(奖励等级)")
                if p_bouns > 0:
                    calc_steps.append(f"-{p_bouns}(惩罚等级)")
                if b_b_bouns > 0:
                    calc_steps.append(f"-{b_b_bouns}(挑战奖励等级)")
                if b_p_bouns > 0:
                    calc_steps.append(f"+{b_p_bouns}(挑战惩罚等级)")
                if d20_challenge_bonus != 0:
                    if back_d20_time >= 2:
                        calc_steps.append(f"{d20_challenge_bonus:+}(挑战大成功/大失败)")  # 自动显示+/-符号
                    else:
                        # 单个d20时根据具体结果显示
                        if back_great_success > 0:
                            calc_steps.append(f"{d20_challenge_bonus:+}(挑战大成功)")
                        elif back_great_fail > 0:
                            calc_steps.append(f"{d20_challenge_bonus:+}(挑战大失败)")
                        else:
                            # 理论上不会走到这里，但可以作为保护
                            calc_steps.append(f"{d20_challenge_bonus:+}(挑战调整)")
                # 只有存在计算步骤时才显示过程
                if calc_steps:
                    success_text = str(original_success_level) + "".join(calc_steps) + f"={success_level}"
                else:
                    success_text = str(success_level)

                dictTValue['tSuccessLevelInt'] = success_text
                dictTValue['tSuccessLevel'] = OlivaDiceCore.msgCustomManager.formatReplySTR(
                    dictStrCustom['strShSuccessLevel'], 
                    dictTValue
                )
            else:
                dictTValue['tSuccessLevel'] = ''
            
            # 根据是否暗骰选择回复方式
            if is_at:
                if flag_hide and flag_is_from_group:
                    dictTValue['tGroupId'] = str(plugin_event.data.group_id)
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strShHideAtOther'], dictTValue)
                    replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strShHideShowAtOther'], dictTValue))
                    OlivaDiceCore.msgReply.replyMsgPrivateByEvent(plugin_event, tmp_reply_str)
                else:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strShResultAtOther'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
            else:
                if flag_hide and flag_is_from_group:
                    dictTValue['tGroupId'] = str(plugin_event.data.group_id)
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strShHide'], dictTValue)
                    replyMsg(plugin_event, OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strShHideShow'], dictTValue))
                    OlivaDiceCore.msgReply.replyMsgPrivateByEvent(plugin_event, tmp_reply_str)
                else:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strShResult'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)

def format_long_dice_rolls(detail_string):
    """
    一个新的辅助函数，用于优化显示效果。
    当每一次掷骰细节超过50个时，花括号内只显示第一个和最后一个，中间用+...+来表示。
    """
    # 确保处理的是字符串类型
    if not isinstance(detail_string, str):
        return detail_string

    def replacer(match):
        # 获取花括号内的完整内容，例如 "2+1+1+..."
        content = match.group(1)
        rolls = content.split('+')
        if len(rolls) > 50:
            return f"{{{rolls[0]}+...+{rolls[-1]}}}"
        else:
            return match.group(0)
    return re.sub(r'\{([^\}]+)\}', replacer, detail_string)

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

def calculate_d20_success_level(rd_object):
    """
    计算挑战值中d20的大成功/大失败：大成功-1，大失败+1
    """
    if not rd_object or not rd_object.resDetailData:
        return 0, 0, 0, 0

    bonus = 0
    great_success = 0
    great_fail = 0
    d20_time = 0
    # 使用一个栈(list)来进行深度优先遍历，以处理复杂的嵌套表达式
    nodes_to_visit = list(rd_object.resDetailData)

    while nodes_to_visit:
        node = nodes_to_visit.pop()

        # 如果节点是列表，将其所有元素添加到待访问栈中
        if isinstance(node, list):
            nodes_to_visit.extend(node)
            continue

        # 如果节点是字典，检查其内容
        if isinstance(node, dict):
            # 检查这是否是一个骰点(d)操作的节点
            if 'key' in node and isinstance(node['key'], dict) and node['key'].get('op') == 'd':
                # 检查骰子的面数是否为20
                if node['key'].get('r') == 20:
                    # 检查并获取骰点结果
                    if 'result' in node and isinstance(node['result'], list) and len(node['result']) > 0:
                        dice_rolls = node['result'][0]
                        if isinstance(dice_rolls, list):
                            for roll in dice_rolls:
                                if isinstance(roll, int):
                                    d20_time += 1
                                    if roll <= 1:
                                        bonus += 1
                                        great_fail += 1
                                    elif roll >= 20:
                                        bonus -= 1
                                        great_success += 1
            
            # 为了处理嵌套结构（如括号内的表达式），将字典中的所有子字典或列表也加入待访问栈
            for value in node.values():
                if isinstance(value, (dict, list)):
                    nodes_to_visit.append(value)
    return bonus, great_success, great_fail, d20_time

def to_half_width(res):
    """
    将字符串中的全角符号转换为半角符号
    """
    result = []
    for char in res:
        code = ord(char)
        # 全角空格
        if code == 0x3000:
            code = 0x0020
        # 全角字符（除空格外）
        elif 0xFF01 <= code <= 0xFF5E:
            code -= 0xFEE0
        result.append(chr(code))
    return ''.join(result)