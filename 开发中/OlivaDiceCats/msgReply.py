# -*- encoding: utf-8 -*-
'''
这里写你的回复。注意插件前置：OlivaDiceCore，写命令请跳转到第146行。
'''

import OlivOS
import OlivaDiceCats
import OlivaDiceCore

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

def parse_at_user(plugin_event, tmp_reast_str, valDict, flag_is_from_group_admin):
    """
    解析消息中的@用户并检查权限
    返回: is_at, at_user_id, cleaned_message_str
    """
    flag_is_from_master = valDict['flag_is_from_master']
    dictTValue = valDict['dictTValue']
    dictStrCustom = valDict['dictStrCustom']
    tmp_reast_str_para = OlivOS.messageAPI.Message_templet('old_string', tmp_reast_str)
    at_user_id = None
    new_tmp_reast_str_parts = []
    is_at = False
    
    for part in tmp_reast_str_para.data:
        if isinstance(part, OlivOS.messageAPI.PARA.at):
            at_user_id = part.data['id']
            tmp_userName01 = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = at_user_id,
                userType = 'user',
                platform = plugin_event.platform['platform'],
                userConfigKey = 'userName',
                botHash = plugin_event.bot_info.hash
            )
            plres = plugin_event.get_stranger_info(at_user_id)
            if plres['active']:
                dictTValue['tUserName01'] = plres['data']['name']
            else:
                dictTValue['tUserName01'] = tmp_userName01
            is_at = True
        else:
            if isinstance(part, OlivOS.messageAPI.PARA.text):
                new_tmp_reast_str_parts.append(part.data['text'])
    
    # 返回解析结果
    cleaned_message = ''.join(new_tmp_reast_str_parts).strip()
    return is_at, at_user_id, cleaned_message

def parse_expression_and_params(expr_str, isMatchWordStart, getMatchWordStartRight, skipSpaceStart):
    """
    解析表达式开头的参数 b/p、u/d、l
    采用与狩魂者插件相同的解析逻辑
    返回: cleaned_expr, bonus_level, luck_modifier, luck_fixed
    """
    bonus_level = 0  # b/p参数影响成功等级
    luck_modifier = 0  # u/d参数影响幸运骰数量
    luck_fixed = None  # l参数固定幸运骰数量，优先级高于u/d
    tmp_reast_str = expr_str
    
    # 循环处理所有参数
    while tmp_reast_str:
        original_str = tmp_reast_str
        
        # 处理b参数（奖励等级）
        if isMatchWordStart(tmp_reast_str, 'b'):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'b')
            # 检查是否有数字指定，只取一位
            if len(tmp_reast_str) > 0 and tmp_reast_str[0].isdigit():
                bonus_level += int(tmp_reast_str[0])
                tmp_reast_str = tmp_reast_str[1:]
            else:
                bonus_level += 1  # 默认为1
            # 移除可能的+号
            if len(tmp_reast_str) > 0 and tmp_reast_str[0] == '+':
                tmp_reast_str = tmp_reast_str[1:]
            continue
        
        # 处理p参数（惩罚等级）
        elif isMatchWordStart(tmp_reast_str, 'p'):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'p')
            # 检查是否有数字指定，只取一位
            if len(tmp_reast_str) > 0 and tmp_reast_str[0].isdigit():
                bonus_level -= int(tmp_reast_str[0])
                tmp_reast_str = tmp_reast_str[1:]
            else:
                bonus_level -= 1  # 默认为1
            # 移除可能的+号
            if len(tmp_reast_str) > 0 and tmp_reast_str[0] == '+':
                tmp_reast_str = tmp_reast_str[1:]
            continue
        
        # 处理u参数（增加幸运骰）
        elif isMatchWordStart(tmp_reast_str, 'u'):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'u')
            # 检查是否有数字指定，只取一位
            if len(tmp_reast_str) > 0 and tmp_reast_str[0].isdigit():
                luck_modifier += int(tmp_reast_str[0])
                tmp_reast_str = tmp_reast_str[1:]
            else:
                luck_modifier += 1  # 默认为1
            # 移除可能的+号
            if len(tmp_reast_str) > 0 and tmp_reast_str[0] == '+':
                tmp_reast_str = tmp_reast_str[1:]
            continue
        
        # 处理d参数（减少幸运骰）
        elif isMatchWordStart(tmp_reast_str, 'd'):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'd')
            # 检查是否有数字指定，只取一位
            if len(tmp_reast_str) > 0 and tmp_reast_str[0].isdigit():
                luck_modifier -= int(tmp_reast_str[0])
                tmp_reast_str = tmp_reast_str[1:]
            else:
                luck_modifier -= 1  # 默认为1
            # 移除可能的+号
            if len(tmp_reast_str) > 0 and tmp_reast_str[0] == '+':
                tmp_reast_str = tmp_reast_str[1:]
            continue
        
        # 处理l参数（固定幸运骰数量）
        elif isMatchWordStart(tmp_reast_str, 'l'):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'l')
            # 检查是否有数字指定，只取一位
            if len(tmp_reast_str) > 0 and tmp_reast_str[0].isdigit():
                luck_fixed = max(1, min(5, int(tmp_reast_str[0])))  # 限制在1-5之间
                tmp_reast_str = tmp_reast_str[1:]
            else:
                luck_fixed = 1  # 默认为1
            # 移除可能的+号
            if len(tmp_reast_str) > 0 and tmp_reast_str[0] == '+':
                tmp_reast_str = tmp_reast_str[1:]
            continue
        
        # 如果没有匹配到任何参数，跳出循环
        if tmp_reast_str == original_str:
            break
    
    # 跳过空格并返回清理后的表达式
    cleaned_expr = skipSpaceStart(tmp_reast_str)
    
    return cleaned_expr, bonus_level, luck_modifier, luck_fixed

def get_pc_luck_value(plugin_event, user_id, tmp_hagID):
    """
    获取人物卡的幸运值
    """
    try:
        tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(user_id, plugin_event.platform['platform'])
        tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(tmp_pcHash, tmp_hagID)
        if tmp_pc_name:
            pc_skills = OlivaDiceCore.pcCard.pcCardDataGetByPcName(tmp_pcHash, hagId=tmp_hagID)
            if pc_skills and '幸运' in pc_skills:
                return max(1, min(5, int(pc_skills['幸运'])))
    except:
        pass
    return 1  # 默认幸运值为1

def update_pc_luck_and_skill(plugin_event, user_id, tmp_hagID, luck_change, upgrade_points_change=1):
    """
    更新人物卡的幸运和升级点
    """
    try:
        tmp_pc_platform = plugin_event.platform['platform']
        tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(user_id, tmp_pc_platform)
        tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(tmp_pcHash, tmp_hagID)
        
        if not tmp_pc_name:
            return  # 没有人物卡就不更新
        
        # 更新幸运值
        if luck_change != 0:
            tmp_luck_old = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                tmp_pcHash,
                '幸运',
                hagId=tmp_hagID
            )
            current_luck = int(tmp_luck_old) if tmp_luck_old is not None else 1
            new_luck = max(1, min(5, current_luck + int(luck_change)))
            
            OlivaDiceCore.pcCard.pcCardDataSetBySkillName(
                tmp_pcHash,
                '幸运',
                new_luck,
                tmp_pc_name,
                hagId=tmp_hagID
            )
        
        # 更新升级点数
        if upgrade_points_change != 0:
            tmp_skill_old = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                tmp_pcHash,
                '升级点',
                hagId=tmp_hagID
            )
            current_skill = int(tmp_skill_old) if tmp_skill_old is not None else 0
            new_skill = current_skill + int(upgrade_points_change)
            
            OlivaDiceCore.pcCard.pcCardDataSetBySkillName(
                tmp_pcHash,
                '升级点',
                new_skill,
                tmp_pc_name,
                hagId=tmp_hagID
            )
    except:
        pass

def roll_luck_dice(luck_count, tmp_template_customDefault=None):
    """
    投掷幸运骰子，自动处理10/1的重投
    返回: (可选择骰子结果列表, 投掷过程详情列表, 大成功数量, 大失败数量, 是否需要手动选择, 确定的结果, 所有详情列表, 带序号的所有详情)
    """
    selectable_results = []  # 可以选择的骰子
    selectable_display_details = []  # 可选择骰子的显示详情（包含重投过程）
    all_details = []  # 所有骰子的详情（包括大成功/大失败）
    all_details_with_index = []  # 带序号的所有骰子详情
    critical_success_count = 0
    critical_failure_count = 0
    confirmed_result = None  # 如果有确定的大成功/大失败结果

    
    for i in range(luck_count):
        rd = OlivaDiceCore.onedice.RD('1d10', tmp_template_customDefault)
        rd.roll()
        if rd.resError is None:
            original_result = int(rd.resInt)  # 保存原始结果
            result = original_result  # 用于选择的结果（保持原始值）
            detail_parts = [f"{original_result}"]
            is_critical = False
            
            # 检查是否需要重投
            if original_result == 10:
                # 重投检查大成功
                rd_reroll = OlivaDiceCore.onedice.RD('1d10', tmp_template_customDefault)
                rd_reroll.roll()
                if rd_reroll.resError is None:
                    reroll_result = int(rd_reroll.resInt)
                    detail_parts.append(f"重投{reroll_result}")
                    if reroll_result == 10:
                        # 大成功，不参与选择
                        critical_success_count += 1
                        detail_parts.append("大成功")
                        is_critical = True
                        if confirmed_result is None:
                            confirmed_result = 10  # 记录一个大成功的结果用于计算
                    # 注意：即使重投不是10，选择时仍然使用原始的10
                else:
                    pass  # 重投失败，保持原值10
            elif original_result == 1:
                # 重投检查大失败
                rd_reroll = OlivaDiceCore.onedice.RD('1d10', tmp_template_customDefault)
                rd_reroll.roll()
                if rd_reroll.resError is None:
                    reroll_result = int(rd_reroll.resInt)
                    detail_parts.append(f"重投{reroll_result}")
                    if reroll_result == 1:
                        # 大失败，不参与选择
                        critical_failure_count += 1
                        detail_parts.append("大失败")
                        is_critical = True
                        if confirmed_result is None:
                            confirmed_result = 1  # 记录一个大失败的结果用于计算
                    # 注意：即使重投不是1，选择时仍然使用原始的1
                else:
                    pass  # 重投失败，保持原值1
            
            # 生成显示字符串
            display_detail = '-'.join(detail_parts)
            all_details.append(display_detail)
            
            # 只有非大成功/大失败的骰子才参与选择
            if not is_critical:
                selectable_results.append(result)
                selectable_display_details.append(display_detail)
            
            # 生成带序号的显示字符串（所有骰子都按投掷顺序显示序号）
            all_details_with_index.append(f"[{i+1}] {display_detail}")
        else:
            # 投掷出错，默认为1并参与选择
            display_detail = "1"
            selectable_results.append(1)
            selectable_display_details.append(display_detail)
            all_details.append(display_detail)
            all_details_with_index.append(f"[{i+1}] {display_detail}")
    
    # 判断是否需要手动选择
    need_manual_selection = True
    if critical_success_count > critical_failure_count:
        # 大成功数量多，直接确定为大成功
        need_manual_selection = False
    elif critical_failure_count > critical_success_count:
        # 大失败数量多，直接确定为大失败
        need_manual_selection = False
    elif critical_success_count == critical_failure_count and (critical_success_count > 0):
        # 大成功和大失败数量相等且都大于0，需要手动选择
        need_manual_selection = True
    else:
        # 没有大成功/大失败，或者只有可选择的骰子，需要手动选择
        need_manual_selection = len(selectable_results) > 0
    
    return selectable_results, selectable_display_details, critical_success_count, critical_failure_count, need_manual_selection, confirmed_result, all_details, all_details_with_index

def determine_critical_result(critical_success_count, critical_failure_count):
    """
    根据大成功和大失败的数量确定最终结果类型
    返回: (结果类型, 幸运变化, 升级点变化)
    """
    if critical_success_count > critical_failure_count:
        # 最终结果为大成功：幸运+1，升级点+1
        return 'critical_success', 1, 1
    elif critical_failure_count > critical_success_count:
        # 最终结果为大失败：幸运-1，升级点+1
        return 'critical_failure', -1, 1
    else:
        # 数量相等或都为0，抵消：幸运和升级点都不变
        return None, 0, 0

def unity_init(plugin_event, Proc):
    # 这里是插件初始化，通常用于加载配置等
    pass

def data_init(plugin_event, Proc):
    # 这里是数据初始化，通常用于加载数据等
    OlivaDiceCats.msgCustomManager.initMsgCustom(Proc.Proc_data['bot_info_dict'])

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
    to_half_width = OlivaDiceCore.msgReply.to_half_width

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
            
        if isMatchWordStart(tmp_reast_str, ['cats'], isCommand = True):
            # 检查是否有等待中的cats选择 - 如果有，阻止新的cats命令执行
            tmp_bothash = plugin_event.bot_info.hash
            tmp_hash = OlivaDiceCore.msgReplyModel.contextRegHash([None, plugin_event.data.user_id])
            if tmp_bothash in OlivaDiceCore.crossHook.dictReplyContextReg and tmp_hash in OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash]:
                del OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash][tmp_hash]
                # tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strCatsInvalidSelection'], dictTValue)
                # replyMsg(plugin_event, tmp_reply_str)
                return
            # 解析@用户
            is_at, at_user_id, tmp_reast_str = parse_at_user(plugin_event, tmp_reast_str, valDict, flag_is_from_group_admin)
            if is_at and not at_user_id:
                return
                
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, 'cats')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            tmp_reast_str = tmp_reast_str.rstrip(' ')
            
            try:
                # 分离前式和后式，如果没有#则默认挑战难度为10
                if '#' in tmp_reast_str:
                    parts = tmp_reast_str.split('#', 1)
                    front_expr = parts[0].strip()
                    back_expr = parts[1].strip()
                else:
                    front_expr = tmp_reast_str.strip()
                    back_expr = '10'
                
                # 解析前式参数
                front_cleaned, front_bonus, front_luck_mod, front_luck_fixed = parse_expression_and_params(front_expr, isMatchWordStart, getMatchWordStartRight, skipSpaceStart)
                # 解析后式参数（后式中的参数效果相反）
                back_cleaned, back_bonus, back_luck_mod, back_luck_fixed = parse_expression_and_params(back_expr, isMatchWordStart, getMatchWordStartRight, skipSpaceStart)
                
                # 确定检定用户
                target_user_id = plugin_event.data.user_id
                
                # 获取人物卡信息
                tmp_pcHash = OlivaDiceCore.pcCard.getPcHash(target_user_id, plugin_event.platform['platform'])
                tmp_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(tmp_pcHash, tmp_hagID)
                
                if tmp_pc_name:
                    dictTValue['tName'] = tmp_pc_name
                else:
                    res = plugin_event.get_stranger_info(user_id = target_user_id)
                    if res != None and res['active']:
                        dictTValue['tName'] = res['data']['name']
                    else:
                        dictTValue['tName'] = f'用户{target_user_id}'
                
                # 设置挑战目标信息
                if is_at:
                    # 获取被@用户的人物卡名称，优先使用人物卡名称
                    challenge_target_name = None
                    at_pcHash = OlivaDiceCore.pcCard.getPcHash(at_user_id, plugin_event.platform['platform'])
                    at_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(at_pcHash, tmp_hagID)
                    
                    if at_pc_name:
                        challenge_target_name = at_pc_name
                    elif 'tUserName01' in dictTValue and dictTValue['tUserName01']:
                        challenge_target_name = dictTValue['tUserName01']
                    else:
                        challenge_target_name = f'用户{at_user_id}'
                    
                    dictTValue['tChallengeTarget'] = f'挑战[{challenge_target_name}]'
                else:
                    dictTValue['tChallengeTarget'] = ''
                
                # 获取人物卡技能数据和规则
                # 前式技能表（自己的技能）
                front_pcHash = OlivaDiceCore.pcCard.getPcHash(plugin_event.data.user_id, plugin_event.platform['platform'])
                front_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(front_pcHash, tmp_hagID)
                front_pc_skills = OlivaDiceCore.pcCard.pcCardDataGetByPcName(front_pcHash, hagId=tmp_hagID) if front_pc_name else {}
                front_skill_valueTable = front_pc_skills.copy()
                
                # 后式技能表（@对方时用对方的技能，否则用自己的技能）
                if is_at:
                    back_pcHash = OlivaDiceCore.pcCard.getPcHash(at_user_id, plugin_event.platform['platform'])
                    back_pc_name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(back_pcHash, tmp_hagID)
                else:
                    back_pcHash = front_pcHash
                    back_pc_name = front_pc_name
                back_pc_skills = OlivaDiceCore.pcCard.pcCardDataGetByPcName(back_pcHash, hagId=tmp_hagID) if back_pc_name else {}
                back_skill_valueTable = back_pc_skills.copy()
                
                # 通用技能表（用于显示和一般用途）
                pc_skills = OlivaDiceCore.pcCard.pcCardDataGetByPcName(tmp_pcHash, hagId=tmp_hagID) if tmp_pc_name else {}
                skill_valueTable = pc_skills.copy()
                
                tmp_pcCardRule = 'default'
                tmp_pcCardRule_new = OlivaDiceCore.pcCard.pcCardDataGetTemplateKey(tmp_pcHash, tmp_pc_name)
                if tmp_pcCardRule_new != None:
                    tmp_pcCardRule = tmp_pcCardRule_new
                
                # 添加映射记录
                if tmp_pc_name != None:
                    skill_valueTable.update(
                        OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                            pcHash = tmp_pcHash,
                            pcCardName = tmp_pc_name,
                            dataKey = 'mappingRecord',
                            resDefault = {}
                        )
                    )
                if front_pc_name != None:
                    front_skill_valueTable.update(
                        OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                            pcHash = front_pcHash,
                            pcCardName = front_pc_name,
                            dataKey = 'mappingRecord',
                            resDefault = {}
                        )
                    )
                if back_pc_name != None:
                    back_skill_valueTable.update(
                        OlivaDiceCore.pcCard.pcCardDataGetTemplateDataByKey(
                            pcHash = back_pcHash,
                            pcCardName = back_pc_name,
                            dataKey = 'mappingRecord',
                            resDefault = {}
                        )
                    )
                
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
                
                # 保存原始技能名（用于后续的技能更新）
                original_back_skill = None
                if back_cleaned and back_cleaned in back_skill_valueTable:
                    original_back_skill = back_cleaned
                
                # 计算前式结果（使用自己的技能）
                front_value = 0
                front_detail = "0"
                if front_cleaned:
                    # 使用replace_skills处理技能替换（前式用自己的技能）
                    front_expr, front_detail = replace_skills(front_cleaned.replace('=', '').replace(' ', ''), front_skill_valueTable, tmp_pcCardRule)
                    
                    # 使用RD处理前式表达式
                    rd_front = OlivaDiceCore.onedice.RD(front_expr, tmp_template_customDefault)
                    rd_front.roll()
                    if rd_front.resError is not None:
                        dictTValue['tRollPara'] = front_cleaned
                        error_msg = OlivaDiceCore.msgReplyModel.get_SkillCheckError(rd_front.resError, dictStrCustom, dictTValue)
                        dictTValue['tResult'] = f"错误的出值：{error_msg}"
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strCatsError'], dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                        return
                    front_value = rd_front.resInt
                    
                    # 显示处理
                    if rd_front.resDetail and rd_front.resDetail != str(rd_front.resInt):
                        if front_detail == rd_front.resDetail:
                            front_detail = f"{front_detail}={front_value}"
                        else:
                            front_detail = f"{front_detail}={rd_front.resDetail}={front_value}"
                    else:
                        if front_detail != str(front_value):
                            front_detail = f"{front_detail}={front_value}"
                        else:
                            front_detail = str(front_value)
                
                # 计算后式结果（@对方时用对方的技能，否则用自己的技能）
                back_value = 10  # 默认挑战难度为10
                back_detail = "10"
                if back_cleaned:
                    # 使用replace_skills处理技能替换（后式根据是否@对方选择技能表）
                    back_expr, back_detail = replace_skills(back_cleaned.replace('=', '').replace(' ', ''), back_skill_valueTable, tmp_pcCardRule)
                    
                    # 使用RD处理后式表达式
                    rd_back = OlivaDiceCore.onedice.RD(back_expr, tmp_template_customDefault)
                    rd_back.roll()
                    if rd_back.resError is not None:
                        dictTValue['tRollPara'] = back_cleaned
                        error_msg = OlivaDiceCore.msgReplyModel.get_SkillCheckError(rd_back.resError, dictStrCustom, dictTValue)
                        dictTValue['tResult'] = f"错误的挑战难度：{error_msg}"
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strCatsError'], dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                        return
                    back_value = rd_back.resInt
                    
                    # 显示处理
                    if rd_back.resDetail and rd_back.resDetail != str(rd_back.resInt):
                        if back_detail == rd_back.resDetail:
                            back_detail = f"{back_detail}={back_value}"
                        else:
                            back_detail = f"{back_detail}={rd_back.resDetail}={back_value}"
                    else:
                        if back_detail != str(back_value):
                            back_detail = f"{back_detail}={back_value}"
                        else:
                            back_detail = str(back_value)
                
                # 获取幸运值并计算幸运骰数量
                luck_value = get_pc_luck_value(plugin_event, target_user_id, tmp_hagID)
                
                # 确定最终幸运骰数量，l参数优先级最高
                final_luck_fixed = back_luck_fixed if back_luck_fixed is not None else front_luck_fixed
                if final_luck_fixed is not None:
                    final_luck_count = final_luck_fixed
                else:
                    total_luck_modifier = front_luck_mod - back_luck_mod  # 后式中的u/d效果相反
                    final_luck_count = max(1, min(5, luck_value + total_luck_modifier))
                
                # 投掷幸运骰
                luck_dice_results, luck_dice_display_details, critical_success_count, critical_failure_count, need_manual_selection, confirmed_result, all_details, all_details_with_index = roll_luck_dice(final_luck_count, tmp_template_customDefault)
                
                # 格式化幸运骰显示
                if need_manual_selection and len(luck_dice_results) > 0:
                    # 需要手动选择时，显示可选择的骰子（包含重投过程）
                    dice_display = []
                    for i, display_detail in enumerate(luck_dice_display_details):
                        dice_display.append(f"[{i+1}] {display_detail}")
                    dictTValue['tLuckDiceList'] = ' '.join(dice_display)
                    dictTValue['tLuckValue'] = str(len(luck_dice_results))
                else:
                    # 自动确定结果时，显示所有骰子详情（带序号）
                    dictTValue['tLuckDiceList'] = ' '.join(all_details_with_index)
                    dictTValue['tLuckValue'] = str(final_luck_count)
                
                # 确定是否需要手动选择
                selected_dice = None
                selected_detail = None
                selected_index = 0
                critical_type = None
                luck_change = 0
                upgrade_points_change = 0
                
                if not need_manual_selection:
                    # 自动确定结果：大成功数量不等于大失败数量
                    critical_type, luck_change, upgrade_points_change = determine_critical_result(critical_success_count, critical_failure_count)
                    
                    # 使用确定的结果（如果没有可选择骰子的话）
                    if confirmed_result is not None:
                        selected_dice = confirmed_result
                        selected_detail = f"幸运骰({confirmed_result})"
                    elif len(luck_dice_results) > 0:
                        # 如果还有可选择的骰子，选择第一个
                        selected_dice = luck_dice_results[0]
                        selected_detail = f"幸运骰({luck_dice_display_details[0]})"
                    else:
                        # 兜底情况
                        selected_dice = 5
                        selected_detail = "幸运骰(5)"
                else:
                    # 需要手动选择
                    if len(luck_dice_results) == 0:
                        # 没有可选择的骰子，可能所有都是大成功/大失败，按数量相等处理
                        critical_type, luck_change, upgrade_points_change = determine_critical_result(critical_success_count, critical_failure_count)
                        selected_dice = confirmed_result if confirmed_result is not None else 5
                        selected_detail = f"幸运骰({selected_dice})"
                    else:
                        # 显示幸运骰并等待选择
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strCatsLuckDice'], dictTValue)
                        replyMsg(plugin_event, tmp_reply_str)
                        
                        # 等待用户选择
                        tmp_select = OlivaDiceCore.msgReplyModel.replyCONTEXT_regWait(
                            plugin_event = plugin_event,
                            flagBlock = 'allowCommand',
                            hash = OlivaDiceCore.msgReplyModel.contextRegHash([None, plugin_event.data.user_id])
                        )
                    
                        # 处理选择结果
                        if type(tmp_select) == str and tmp_select.isdigit():
                            tmp_select_int = int(tmp_select) - 1
                            if tmp_select_int >= 0 and tmp_select_int < len(luck_dice_results):
                                selected_index = tmp_select_int
                                if tmp_bothash in OlivaDiceCore.crossHook.dictReplyContextReg and tmp_hash in OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash]:
                                    del OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash][tmp_hash]
                            else:
                                # 无效输入，返回错误信息
                                if tmp_bothash in OlivaDiceCore.crossHook.dictReplyContextReg and tmp_hash in OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash]:
                                    del OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash][tmp_hash]
                                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strCatsInvalidSelection'], dictTValue)
                                replyMsg(plugin_event, tmp_reply_str)
                                return
                        elif tmp_select == None:
                            # 超时情况
                            if tmp_bothash in OlivaDiceCore.crossHook.dictReplyContextReg and tmp_hash in OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash]:
                                del OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash][tmp_hash]
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strCatsInvalidSelection'], dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
                            return
                        else:
                            # 无效输入
                            if tmp_bothash in OlivaDiceCore.crossHook.dictReplyContextReg and tmp_hash in OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash]:
                                del OlivaDiceCore.crossHook.dictReplyContextReg[tmp_bothash][tmp_hash]
                            tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strCatsInvalidSelection'], dictTValue)
                            replyMsg(plugin_event, tmp_reply_str)
                            return
                        
                        # 获取选择的骰子结果
                        selected_dice = luck_dice_results[selected_index]
                        selected_detail = f"幸运骰({luck_dice_display_details[selected_index]})"
                    
                    # 手动选择情况下，根据大成功/大失败的最终结果计算幸运和升级点变化
                    _, luck_change, upgrade_points_change = determine_critical_result(critical_success_count, critical_failure_count)
                
                # 计算最终结果
                total_result = front_value + selected_dice
                success_level = total_result - back_value
                
                # 应用b/p参数
                final_bonus = front_bonus - back_bonus  # 后式中的b/p效果相反
                final_success_level = success_level + final_bonus
                
                # 构建显示过程
                # 前式过程显示
                front_process = front_detail
                
                # 后式过程显示
                back_process = back_detail
                
                # 幸运骰显示（只显示结果，不显示投掷过程）
                luck_display = selected_detail
                
                # 重投信息处理（从幸运骰详情中提取）
                reroll_info = ""
                if critical_success_count > 0 or critical_failure_count > 0:
                    reroll_parts = []
                    if critical_success_count > 0:
                        reroll_parts.append(f"大成功×{critical_success_count}")
                    if critical_failure_count > 0:
                        reroll_parts.append(f"大失败×{critical_failure_count}")
                    reroll_info = f"重投结果: {', '.join(reroll_parts)}\n"
                    
                # 设置显示值
                dictTValue['tFrontResult'] = front_process
                dictTValue['tLuckDiceResult'] = luck_display
                dictTValue['tTotalResult'] = str(total_result)
                dictTValue['tBackResult'] = back_process
                dictTValue['tSuccessLevelInt'] = str(final_success_level)
                dictTValue['tRerollInfo'] = reroll_info
                
                # 判断技能检定类型
                tmpSkillCheckType = OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FAIL
                
                # 处理大成功/大失败
                if critical_type == 'critical_success':
                    tmpSkillCheckType = OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_SUCCESS
                elif critical_type == 'critical_failure':
                    tmpSkillCheckType = OlivaDiceCore.skillCheck.resultType.SKILLCHECK_GREAT_FAIL
                else:
                    # 正常检定结果
                    if final_success_level >= 0:
                        tmpSkillCheckType = OlivaDiceCore.skillCheck.resultType.SKILLCHECK_SUCCESS
                    else:
                        tmpSkillCheckType = OlivaDiceCore.skillCheck.resultType.SKILLCHECK_FAIL
                
                # 获取技能检定结果文案
                dictTValue['tSkillCheckReasult'] = OlivaDiceCore.msgReplyModel.get_SkillCheckResult(tmpSkillCheckType, dictStrCustom, dictTValue)
                
                # 更新人物卡的幸运值和升级点（只有在有变化时才更新）
                if luck_change != 0 or upgrade_points_change != 0:
                    update_pc_luck_and_skill(plugin_event, tmp_userID, tmp_hagID, luck_change, upgrade_points_change)
                
                # 根据是否自动确定结果选择不同的回复模板
                if not need_manual_selection and (critical_type == 'critical_success' or critical_type == 'critical_failure'):
                    # 直接大成功/大失败，使用简化模板，显示所有骰子详情
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strCatsCriticalResult'], dictTValue)
                else:
                    # 正常检定或手动选择后的结果，使用完整模板
                    dictTValue['tSuccessLevel'] = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strCatsSuccessLevel'], dictTValue)
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strCatsResult'], dictTValue)
                
                replyMsg(plugin_event, tmp_reply_str)
                
            except Exception as e:
                dictTValue['tResult'] = str(e)
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strCatsError'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
            
            return
