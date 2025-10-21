# -*- encoding: utf-8 -*-
'''
群管功能回复处理
'''

import OlivOS
import OlivaDiceManager
import OlivaDiceCore
import json
import requests
import os

def unity_init(plugin_event, Proc):
    # 插件初始化
    pass

def data_init(plugin_event, Proc):
    # 数据初始化
    OlivaDiceManager.msgCustomManager.initMsgCustom(Proc.Proc_data['bot_info_dict'])

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
    tmp_id_str = str(plugin_event.base_info['self_id'])
    tmp_at_str_sub = None
    tmp_id_str_sub = None
    if 'sub_self_id' in plugin_event.data.extend:
        if plugin_event.data.extend['sub_self_id'] != None:
            tmp_at_str_sub = OlivOS.messageAPI.PARA.at(plugin_event.data.extend['sub_self_id']).CQ()
            tmp_id_str_sub = str(plugin_event.data.extend['sub_self_id'])
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
    
    if flag_force_reply is False:
        tmp_reast_str_old = tmp_reast_str
        tmp_reast_obj = OlivOS.messageAPI.Message_templet(
            'old_string',
            tmp_reast_str
        )
        tmp_at_list = []
        for tmp_reast_obj_this in tmp_reast_obj.data:
            tmp_para_str_this = tmp_reast_obj_this.CQ()
            if type(tmp_reast_obj_this) is OlivOS.messageAPI.PARA.at:
                tmp_at_list.append(str(tmp_reast_obj_this.data['id']))
                tmp_reast_str = tmp_reast_str.lstrip(tmp_para_str_this)
            elif type(tmp_reast_obj_this) is OlivOS.messageAPI.PARA.text:
                if tmp_para_str_this.strip(' ') == '':
                    tmp_reast_str = tmp_reast_str.lstrip(tmp_para_str_this)
                else:
                    break
            else:
                break
        if tmp_id_str in tmp_at_list:
            flag_force_reply = True
        if tmp_id_str_sub in tmp_at_list:
            flag_force_reply = True
        if 'all' in tmp_at_list:
            flag_force_reply = True
        if flag_force_reply is True:
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
        else:
            tmp_reast_str = tmp_reast_str_old
    
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
        
        # 此频道关闭时中断处理
        if not flag_hostLocalEnable and not flag_force_reply:
            return
        # 此群关闭时中断处理
        if not flag_groupEnable and not flag_force_reply:
            return
        
        # 权限检查函数
        def check_permission():
            return flag_is_from_group_admin or flag_is_from_master
        
        # 获取用户名称函数
        def get_user_name(user_id):
            """获取用户名称"""
            user_name = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = user_id,
                userType = 'user',
                platform = plugin_event.platform['platform'],
                userConfigKey = 'userName',
                botHash = plugin_event.bot_info.hash
            )
            # 没获取到再用api获取
            if user_name == None:
                plres = plugin_event.get_stranger_info(user_id)
                if plres != None and 'active' in plres and plres['active']:
                    user_name = plres['data']['name']
                else:
                    user_name = f'用户{user_id}'
            return user_name
        
        # 解析@用户函数
        def parse_at_user(message_str):
            """解析消息中的@用户,返回(用户ID列表, 去除@后的消息)"""
            tmp_msg_obj = OlivOS.messageAPI.Message_templet('old_string', message_str)
            user_ids = []
            remaining_msg = message_str
            
            for msg_part in tmp_msg_obj.data:
                if type(msg_part) is OlivOS.messageAPI.PARA.at:
                    user_id = str(msg_part.data['id'])
                    user_ids.append(user_id)
                    # 从消息中移除这个@
                    remaining_msg = remaining_msg.replace(msg_part.CQ(), '', 1)
            
            return user_ids, remaining_msg.strip()
        
        # 获取账号配置(用于调用API)
        def get_account_config():
            """从 conf/account.json 读取账号配置"""
            config_path = os.path.join('conf', 'account.json')
            try:
                if not os.path.exists(config_path):
                    return None
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                if 'account' not in config_data or not config_data['account']:
                    return None
                
                current_bot_id = str(plugin_event.bot_info.id)
                for account_config in config_data['account']:
                    if 'id' in account_config and str(account_config['id']) == current_bot_id:
                        if 'server' not in account_config:
                            return None
                        server_config = account_config['server']
                        required_fields = ['host', 'port', 'access_token']
                        for field in required_fields:
                            if field not in server_config:
                                return None
                        return server_config
                return None
            except Exception as e:
                return None
        
        # 调用API发送群公告
        def send_group_notice(group_id, content):
            """发送群公告"""
            server_config = get_account_config()
            if not server_config:
                return False
            
            forward_data = {
                "Host": server_config["host"].replace("http://", "").replace("https://", ""),
                "Port": server_config["port"],
                "AccessToken": server_config["access_token"]
            }
            
            api_url = f"http://{forward_data['Host']}:{forward_data['Port']}/_send_group_notice"
            payload = {
                "group_id": group_id,
                "content": content
            }
            
            headers = {
                "Authorization": f"Bearer {forward_data['AccessToken']}",
                "Content-Type": "application/json"
            }
            
            try:
                response = requests.post(
                    api_url,
                    data=json.dumps(payload),
                    headers=headers,
                    timeout=5
                )
                return response.status_code == 200
            except Exception:
                return False
        
        # 调用API设置群头衔
        def set_group_special_title(group_id, user_id, special_title):
            """设置群头衔"""
            server_config = get_account_config()
            if not server_config:
                return False
            
            forward_data = {
                "Host": server_config["host"].replace("http://", "").replace("https://", ""),
                "Port": server_config["port"],
                "AccessToken": server_config["access_token"]
            }
            
            api_url = f"http://{forward_data['Host']}:{forward_data['Port']}/set_group_special_title"
            payload = {
                "group_id": group_id,
                "user_id": user_id,
                "special_title": special_title
            }
            
            headers = {
                "Authorization": f"Bearer {forward_data['AccessToken']}",
                "Content-Type": "application/json"
            }
            
            try:
                response = requests.post(
                    api_url,
                    data=json.dumps(payload),
                    headers=headers,
                    timeout=5
                )
                return response.status_code == 200
            except Exception:
                return False
        
        '''命令处理开始'''
        
        # 设置命令系列
        if isMatchWordStart(tmp_reast_str, '设置', isCommand=True):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, '设置')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)

            # 1. 名片
            if isMatchWordStart(tmp_reast_str, ['名片','群名片']):
                if not flag_is_from_group:
                    replyMsg(plugin_event, dictStrCustom['strForGroupOnly'])
                    return
                
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['名片','群名片'])
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                
                # 解析@用户
                user_ids, content = parse_at_user(tmp_reast_str)
                
                # 判断是否为自己
                target_user_id = None
                if '自己' in tmp_reast_str or not user_ids:
                    target_user_id = plugin_event.data.user_id
                    # 提取内容(去除"自己")
                    content = tmp_reast_str.replace('自己', '').strip()
                else:
                    if not check_permission():
                        replyMsg(plugin_event, dictStrCustom['strNeedAdmin'])
                        return
                    target_user_id = user_ids[0]
                
                if not content:
                    replyMsg(plugin_event, dictStrCustom['strNoContent'])
                    return
                
                # 获取目标用户名称并设置变量
                dictTValue['tTargetName'] = get_user_name(target_user_id)
                dictTValue['tContent'] = content
                
                try:
                    plugin_event.set_group_card(
                        group_id=plugin_event.data.group_id,
                        user_id=target_user_id,
                        card=content
                    )
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strCardSetSuccess'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                except:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strCardSetFailed'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                return
            
            # 2. 群名
            elif isMatchWordStart(tmp_reast_str, '群名'):
                if not flag_is_from_group:
                    replyMsg(plugin_event, dictStrCustom['strForGroupOnly'])
                    return
                if not check_permission():
                    replyMsg(plugin_event, dictStrCustom['strNeedAdmin'])
                    return
                
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, '群名')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                group_name = tmp_reast_str.strip()
                
                if not group_name:
                    replyMsg(plugin_event, dictStrCustom['strNoContent'])
                    return
                
                try:
                    plugin_event.set_group_name(
                        group_id=plugin_event.data.group_id,
                        group_name=group_name
                    )
                    replyMsg(plugin_event, dictStrCustom['strGroupNameSetSuccess'])
                except:
                    replyMsg(plugin_event, dictStrCustom['strGroupNameSetFailed'])
                return
            
            # 3. 管理员
            elif isMatchWordStart(tmp_reast_str, '管理员'):
                if not flag_is_from_group:
                    replyMsg(plugin_event, dictStrCustom['strForGroupOnly'])
                    return
                if not check_permission():
                    replyMsg(plugin_event, dictStrCustom['strNeedAdmin'])
                    return
                
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, '管理员')
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                
                # 解析开启/关闭
                enable = None
                if isMatchWordStart(tmp_reast_str, '添加'):
                    enable = True
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, '添加').strip()
                elif isMatchWordStart(tmp_reast_str, '移除'):
                    enable = False
                    tmp_reast_str = getMatchWordStartRight(tmp_reast_str, '移除').strip()
                
                if enable is None:
                    replyMsg(plugin_event, dictStrCustom['strAdminParamError'])
                    return
                
                # 解析@用户
                user_ids, _ = parse_at_user(tmp_reast_str)
                if not user_ids:
                    replyMsg(plugin_event, dictStrCustom['strNoTarget'])
                    return
                
                # 获取目标用户名称
                target_user_id = user_ids[0]
                dictTValue['tTargetName'] = get_user_name(target_user_id)
                
                try:
                    plugin_event.set_group_admin(
                        group_id=plugin_event.data.group_id,
                        user_id=target_user_id,
                        enable=enable
                    )
                    if enable:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strAdminSetSuccess'], dictTValue)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strAdminRemoveSuccess'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                except:
                    if enable:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strAdminSetFailed'], dictTValue)
                    else:
                        tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strAdminRemoveFailed'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                return
            
            # 4. 头衔
            elif isMatchWordStart(tmp_reast_str, ['头衔','群头衔']):
                if not flag_is_from_group:
                    replyMsg(plugin_event, dictStrCustom['strForGroupOnly'])
                    return
                # 设置头衔永远需要权限
                if not check_permission():
                    replyMsg(plugin_event, dictStrCustom['strNeedAdmin'])
                    return
                
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['头衔','群头衔'])
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                
                # 解析@用户
                user_ids, content = parse_at_user(tmp_reast_str)
                
                # 判断是否为自己(没有@用户时默认自己)
                target_user_id = None
                if '自己' in tmp_reast_str or not user_ids:
                    target_user_id = plugin_event.data.user_id
                    # 提取内容(去除"自己")
                    content = tmp_reast_str.replace('自己', '').strip()
                else:
                    target_user_id = user_ids[0]
                
                if not content:
                    replyMsg(plugin_event, dictStrCustom['strNoContent'])
                    return
                
                # 获取目标用户名称并设置变量
                dictTValue['tTargetName'] = get_user_name(target_user_id)
                dictTValue['tContent'] = content
                
                # 使用API调用设置群头衔
                result = set_group_special_title(
                    plugin_event.data.group_id,
                    target_user_id,
                    content
                )
                
                if result:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strTitleSetSuccess'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                else:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strTitleSetFailed'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                return
            
            # 5. 公告
            elif isMatchWordStart(tmp_reast_str, ['公告','群公告']):
                if not flag_is_from_group:
                    replyMsg(plugin_event, dictStrCustom['strForGroupOnly'])
                    return
                if not check_permission():
                    replyMsg(plugin_event, dictStrCustom['strNeedAdmin'])
                    return
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['公告','群公告'])
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                content = tmp_reast_str.strip()
                
                if not content:
                    replyMsg(plugin_event, dictStrCustom['strNoContent'])
                    return
                
                result = send_group_notice(plugin_event.data.group_id, content)
                if result:
                    replyMsg(plugin_event, dictStrCustom['strNoticeSuccess'])
                else:
                    replyMsg(plugin_event, dictStrCustom['strNoticeFailed'])
                return
        
        # 6. 全员禁言
        elif isMatchWordStart(tmp_reast_str, '全员禁言', isCommand=True):
            if not flag_is_from_group:
                replyMsg(plugin_event, dictStrCustom['strForGroupOnly'])
                return
            if not check_permission():
                replyMsg(plugin_event, dictStrCustom['strNeedAdmin'])
                return
            
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, '全员禁言')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            
            # 解析1/0或开启/关闭
            enable = None
            if isMatchWordStart(tmp_reast_str, '开启'):
                enable = True
            elif isMatchWordStart(tmp_reast_str, '关闭'):
                enable = False
            
            if enable is None:
                replyMsg(plugin_event, dictStrCustom['strGroupBanParamError'])
                return
            
            try:
                plugin_event.set_group_whole_ban(
                    group_id=plugin_event.data.group_id,
                    enable=enable
                )
                replyMsg(plugin_event, dictStrCustom['strGroupBanSuccess'])
            except:
                replyMsg(plugin_event, dictStrCustom['strGroupBanFailed'])
            return
        
        # 7. 取消命令系列
        elif isMatchWordStart(tmp_reast_str, '取消', isCommand=True):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, '取消')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            
            # 7.1 取消头衔
            if isMatchWordStart(tmp_reast_str, ['头衔','群头衔']):
                if not flag_is_from_group:
                    replyMsg(plugin_event, dictStrCustom['strForGroupOnly'])
                    return
                # 取消头衔永远需要权限
                if not check_permission():
                    replyMsg(plugin_event, dictStrCustom['strNeedAdmin'])
                    return
                
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['头衔','群头衔'])
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                
                # 解析@用户
                user_ids, _ = parse_at_user(tmp_reast_str)
                
                # 判断是否为自己(没有@用户时默认自己)
                target_user_id = None
                if '自己' in tmp_reast_str or not user_ids:
                    target_user_id = plugin_event.data.user_id
                else:
                    target_user_id = user_ids[0]
                
                # 获取目标用户名称并设置变量
                dictTValue['tTargetName'] = get_user_name(target_user_id)
                
                # 使用API调用取消群头衔(传空字符串)
                result = set_group_special_title(
                    plugin_event.data.group_id,
                    target_user_id,
                    ""  # 空字符串表示取消头衔
                )
                
                if result:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strTitleRemoveSuccess'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                else:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strTitleRemoveFailed'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                return
            
            # 7.2 取消禁言
            elif isMatchWordStart(tmp_reast_str, ['禁言','解除禁言']):
                if not flag_is_from_group:
                    replyMsg(plugin_event, dictStrCustom['strForGroupOnly'])
                    return
                if not check_permission():
                    replyMsg(plugin_event, dictStrCustom['strNeedAdmin'])
                    return
                
                tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['禁言','解除禁言'])
                tmp_reast_str = skipSpaceStart(tmp_reast_str)
                
                # 解析@用户
                user_ids, _ = parse_at_user(tmp_reast_str)
                if not user_ids:
                    replyMsg(plugin_event, dictStrCustom['strNoTarget'])
                    return
                
                # 获取目标用户名称
                target_user_id = user_ids[0]
                dictTValue['tTargetName'] = get_user_name(target_user_id)
                
                try:
                    plugin_event.set_group_ban(
                        group_id=plugin_event.data.group_id,
                        user_id=target_user_id,
                        duration=0  # duration为0表示解除禁言
                    )
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strUnbanSuccess'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                except:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strUnbanFailed'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                return
        
        # 8. 禁言
        elif isMatchWordStart(tmp_reast_str, '禁言', isCommand=True):
            if not flag_is_from_group:
                replyMsg(plugin_event, dictStrCustom['strForGroupOnly'])
                return
            if not check_permission():
                replyMsg(plugin_event, dictStrCustom['strNeedAdmin'])
                return
            
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, '禁言')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            
            # 解析禁言时长(如果有的话)
            ban_duration = 1800  # 默认1800秒(30分钟)
            tmp_parts = tmp_reast_str.split()
            if len(tmp_parts) > 0 and tmp_parts[0].isdigit():
                ban_duration = int(tmp_parts[0])
                # 移除时长参数
                tmp_reast_str = tmp_reast_str[len(tmp_parts[0]):].strip()
            
            # 解析@用户
            user_ids, _ = parse_at_user(tmp_reast_str)
            if not user_ids:
                replyMsg(plugin_event, dictStrCustom['strNoTarget'])
                return
            
            # 获取目标用户名称
            target_user_id = user_ids[0]
            dictTValue['tTargetName'] = get_user_name(target_user_id)
            dictTValue['tContent'] = str(ban_duration)
            
            try:
                plugin_event.set_group_ban(
                    group_id=plugin_event.data.group_id,
                    user_id=target_user_id,
                    duration=ban_duration
                )
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBanSuccess'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
            except:
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strBanFailed'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
            return
        
        # 9. 踢出
        elif isMatchWordStart(tmp_reast_str, ['踢出','踢人'], isCommand=True):
            if not flag_is_from_group:
                replyMsg(plugin_event, dictStrCustom['strForGroupOnly'])
                return
            if not check_permission():
                replyMsg(plugin_event, dictStrCustom['strNeedAdmin'])
                return
            
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['踢出','踢人'])
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            
            # 解析@用户
            user_ids, _ = parse_at_user(tmp_reast_str)
            if not user_ids:
                replyMsg(plugin_event, dictStrCustom['strNoTarget'])
                return
            
            # 获取目标用户名称
            target_user_id = user_ids[0]
            dictTValue['tTargetName'] = get_user_name(target_user_id)
            
            try:
                plugin_event.set_group_kick(
                    group_id=plugin_event.data.group_id,
                    user_id=target_user_id
                )
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strKickSuccess'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
            except:
                tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strKickFailed'], dictTValue)
                replyMsg(plugin_event, tmp_reply_str)
            return
        
        # 10. 点赞
        elif isMatchWordStart(tmp_reast_str, '点赞', isCommand=True):
            tmp_reast_str = getMatchWordStartRight(tmp_reast_str, '点赞')
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
            
            # 解析次数参数(如果有的话)
            like_times = 20  # 默认20次
            tmp_parts = tmp_reast_str.split()
            if len(tmp_parts) > 0 and tmp_parts[0].isdigit():
                like_times = int(tmp_parts[0])
                # 移除次数参数
                tmp_reast_str = tmp_reast_str[len(tmp_parts[0]):].strip()
            
            # 解析@用户
            user_ids, remaining_msg = parse_at_user(tmp_reast_str)
            
            # 判断是否为自己(没有@用户时默认自己)
            target_user_id = None
            is_self = False
            
            if '自己' in tmp_reast_str or not user_ids:
                # 点赞自己,不需要权限
                target_user_id = plugin_event.data.user_id
                is_self = True
            else:
                # 点赞他人,需要权限
                if not check_permission():
                    replyMsg(plugin_event, dictStrCustom['strNeedAdmin'])
                    return
                target_user_id = user_ids[0]
            
            # 获取目标用户名称
            if not is_self:
                dictTValue['tTargetName'] = get_user_name(target_user_id)
            
            dictTValue['tContent'] = str(like_times)
            try:
                plugin_event.send_like(
                    user_id=target_user_id,
                    times=like_times
                )
                if is_self:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strLikeSelfSuccess'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
                else:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strLikeSuccess'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
            except:
                if is_self:
                    replyMsg(plugin_event, dictStrCustom['strLikeFailed'].replace('[{tTargetName}]', '自己'))
                else:
                    tmp_reply_str = OlivaDiceCore.msgCustomManager.formatReplySTR(dictStrCustom['strLikeFailed'], dictTValue)
                    replyMsg(plugin_event, tmp_reply_str)
            return
