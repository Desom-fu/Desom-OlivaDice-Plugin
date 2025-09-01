# -*- encoding: utf-8 -*-
'''
这里写你的回复。注意插件前置：OlivaDiceCore，写命令请跳转到第146行。
'''

import OlivOS
import jrlp
import OlivaDiceCore

import copy
import os
import json
import random
import time

# 定义数据存储路径
DATA_PATH = "plugin/data/jrlp"

def unity_init(plugin_event, Proc):
    # 这里是插件初始化，通常用于加载配置等
    # 创建数据存储目录
    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)

def data_init(plugin_event, Proc):
    # 这里是数据初始化，通常用于加载数据等
    jrlp.msgCustomManager.initMsgCustom(Proc.Proc_data['bot_info_dict'])

def get_today_wife(group_id, user_id):
    """
    获取今日老婆
    """
    # 构建数据文件路径
    group_path = os.path.join(DATA_PATH, str(group_id))
    if not os.path.exists(group_path):
        os.makedirs(group_path)
    
    data_file = os.path.join(group_path, f"{user_id}.json")
    
    # 获取今天日期
    today = time.strftime('%Y-%m-%d', time.localtime())
    
    # 如果文件存在，检查是否是今天的数据
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # 如果是今天的数据，直接返回
        if data.get('date') == today:
            return data.get('qq'), data.get('name'), False  # False表示不是首次抽取
    
    # 如果没有数据或不是今天的数据，重新抽取
    return None, None, True  # True表示需要首次抽取

def save_today_wife(group_id, user_id, qq, name):
    """
    保存今日老婆数据
    """
    group_path = os.path.join(DATA_PATH, str(group_id))
    if not os.path.exists(group_path):
        os.makedirs(group_path)
    
    data_file = os.path.join(group_path, f"{user_id}.json")
    
    data = {
        'date': time.strftime('%Y-%m-%d', time.localtime()),
        'qq': qq,
        'name': name
    }
    
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

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
        # 今日老婆功能实现
        if isMatchWordStart(tmp_reast_str, ['今日老婆', 'jrlp'], isCommand = True):
            # 检查是否在群聊中使用
            if not flag_is_from_group:
                replyMsg(plugin_event, '该命令只能在群聊中使用')
                return
                
            user_id = plugin_event.data.user_id
            group_id = plugin_event.data.group_id
            # 获取群成员列表
            group_member_list = plugin_event.get_group_member_list(group_id)
            if not group_member_list or group_member_list["active"] == False:
                replyMsg(plugin_event, '获取群成员列表失败')
                return
            
            # 获取用户ID
            group_member_list_data = group_member_list["data"]
            
            # 检查是否已经抽取过今日老婆
            wife_qq, wife_name, is_first_draw = get_today_wife(group_id, user_id)
            
            if not is_first_draw and wife_qq and wife_name:
                # 今日已抽取，直接返回结果
                dictTValue['qq'] = str(wife_qq)
                dictTValue['name'] = wife_name
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['jrlpRepeat'], dictTValue)
                if tmp_reply_str != None:
                    replyMsg(plugin_event, tmp_reply_str)
            else:
                # 首次抽取今日老婆
                if not group_member_list_data:
                    replyMsg(plugin_event, '群成员列表为空，无法抽取')
                    return
                
                # 随机选择一个群成员
                chosen_member = random.choice(group_member_list_data)
                wife_qq = chosen_member['user_id']
                wife_name = chosen_member['name']
                if not wife_name:
                    stranger_info = plugin_event.get_stranger_info(wife_qq)
                    wife_name = stranger_info['name']
                    if not wife_name:
                        wife_name = f"哎呀，没能成功获取用户名！"
                
                # 保存抽取结果
                save_today_wife(group_id, user_id, wife_qq, wife_name)
                
                # 构造回复消息
                dictTValue['qq'] = str(wife_qq)
                dictTValue['name'] = wife_name
                url = f"https://q1.qlogo.cn/g?b=qq&nk={wife_qq}&s=640"
                
                # 检查是否抽到了机器人自己
                if wife_qq == plugin_event.base_info['self_id']:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['jrlpRobot'], dictTValue)
                elif wife_qq == user_id:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['jrlpSelf'], dictTValue)
                else:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['jrlpFirst'], dictTValue)
                    
                if tmp_reply_str != None:
                    replyMsg(plugin_event, f"[CQ:image,file={url}]" + tmp_reply_str)
            return
