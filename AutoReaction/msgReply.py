# -*- encoding: utf-8 -*-
'''
QQ号检测表情回复插件
前置插件：OlivaDiceCore
功能：当检测到指定QQ号发送消息时，自动回复多个指定表情
支持三种表情API接口自动切换
'''

import OlivOS
import OlivaDiceCore
import json
import os
import requests
from pathlib import Path

# 数据存储路径
DATA_PATH = "plugin/data/AutoReaction"
# 配置文件路径
CONFIG_FILE = os.path.join(DATA_PATH, "config.json")
WHITELIST_FILE = os.path.join(DATA_PATH, "whitelist.json")
PROTOCOL_FILE = os.path.join(DATA_PATH, "protocol.json")  # 新增协议配置文件

def ensure_data_dir():
    """确保数据目录存在"""
    Path(DATA_PATH).mkdir(parents=True, exist_ok=True)

def load_json_file(file_path, default={}):
    """加载JSON文件"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"加载文件 {file_path} 失败: {e}")
    return default

def save_json_file(file_path, data):
    """保存JSON文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"保存文件 {file_path} 失败: {e}")
        return False

def unity_init(plugin_event, Proc):
    """初始化配置"""
    ensure_data_dir()
    # 初始化默认配置文件
    if not os.path.exists(CONFIG_FILE):
        default_config = {
            "target_users": {}
        }
        save_json_file(CONFIG_FILE, default_config)
    # 初始化白名单文件
    if not os.path.exists(WHITELIST_FILE):
        default_whitelist = {
            "whitelist_groups": []
        }
        save_json_file(WHITELIST_FILE, default_whitelist)
    # 初始化协议文件
    if not os.path.exists(PROTOCOL_FILE):
        default_protocol = {
            "protocol": 1  # 默认使用Lagrange协议
        }
        save_json_file(PROTOCOL_FILE, default_protocol)

def data_init(plugin_event, Proc):
    """数据初始化"""
    pass

def get_account_config(plugin_event):
    """从 conf/account.json 读取账号配置，根据当前bot_id匹配对应账号，失败时返回None"""
    config_path = os.path.join('conf', 'account.json')
    try:
        if not os.path.exists(config_path):
            return None
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        if 'account' not in config_data or not config_data['account']:
            return None
        # 获取当前bot_id
        current_bot_id = str(plugin_event.bot_info.id)
        # 遍历所有账号配置，查找匹配的bot_id
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
        print(f"读取账号配置失败: {e}")
        return None

def get_protocol():
    """获取当前使用的协议"""
    protocol_data = load_json_file(PROTOCOL_FILE)
    return protocol_data.get("protocol", 1)  # 默认为1

def send_reaction_v1(plugin_event, server_config, message_id, reaction_code):
    """Lagrange表情API接口: /set_group_reaction"""
    forward_data = {
        "Type": "Http",
        "Host": server_config["host"].replace("http://", "").replace("https://", ""),
        "Port": server_config["port"],
        "AccessToken": server_config["access_token"]
    }
    
    api_url = f"http://{forward_data['Host']}:{forward_data['Port']}/set_group_reaction"
    payload = {
        "group_id": plugin_event.data.group_id,
        "message_id": message_id,
        "code": reaction_code,
        "is_add": True
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

def send_reaction_v2(plugin_event, server_config, message_id, reaction_code):
    """NapCat表情API接口: /set_msg_emoji_like (数字ID)"""
    forward_data = {
        "Type": "Http",
        "Host": server_config["host"].replace("http://", "").replace("https://", ""),
        "Port": server_config["port"],
        "AccessToken": server_config["access_token"]
    }
    
    api_url = f"http://{forward_data['Host']}:{forward_data['Port']}/set_msg_emoji_like"
    payload = {
        "message_id": message_id,
        "emoji_id": reaction_code,
        "set": True
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
    except (ValueError, Exception):
        return False

def send_reaction_v3(plugin_event, server_config, message_id, reaction_code):
    """LLOneBot表情API接口: /set_msg_emoji_like (字符串ID)"""
    forward_data = {
        "Type": "Http",
        "Host": server_config["host"].replace("http://", "").replace("https://", ""),
        "Port": server_config["port"],
        "AccessToken": server_config["access_token"]
    }
    
    api_url = f"http://{forward_data['Host']}:{forward_data['Port']}/set_msg_emoji_like"
    payload = {
        "message_id": message_id,
        "emoji_id": reaction_code
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

def send_reactions(plugin_event, server_config, message_id, reaction_codes):
    """根据设置的协议发送表情"""
    protocol = get_protocol()
    for code in reaction_codes:
        if protocol == 1:
            if not send_reaction_v1(plugin_event, server_config, message_id, code):
                return False
        elif protocol == 2:
            if not send_reaction_v2(plugin_event, server_config, message_id, code):
                return False
        elif protocol == 3:
            if not send_reaction_v3(plugin_event, server_config, message_id, code):
                return False
        else:
            # 默认使用协议1
            if not send_reaction_v1(plugin_event, server_config, message_id, code):
                return False
    return True

def handle_admin_command(plugin_event, dictTValue, dictStrCustom, tmp_reast_str):
    """处理骰骰主管理命令"""
    replyMsg = OlivaDiceCore.msgReply.replyMsg
    isMatchWordStart = OlivaDiceCore.msgReply.isMatchWordStart
    getMatchWordStartRight = OlivaDiceCore.msgReply.getMatchWordStartRight
    skipSpaceStart = OlivaDiceCore.msgReply.skipSpaceStart
    
    # 加载配置
    config = load_json_file(CONFIG_FILE)
    whitelist = load_json_file(WHITELIST_FILE)
    
    # 设置协议
    if isMatchWordStart(tmp_reast_str, ['回应设置协议'], isCommand=True):
        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['回应设置协议'])
        tmp_reast_str = skipSpaceStart(tmp_reast_str)
        
        if not tmp_reast_str.strip():
            # 显示当前协议选项
            replyMsg(plugin_event, 
                "当前支持的协议:\n"
                "1：Lagrange\n"
                "2：NapCat\n"
                "3：LLOneBot/LLTwoBot\n\n"
                "当前使用的协议: " + str(get_protocol()) + "\n"
                "请输入 .回应设置协议 对应序号 来设置对应的协议"
            )
            return True
        
        try:
            protocol_num = int(tmp_reast_str.strip())
            if protocol_num in [1, 2, 3]:
                protocol_data = {"protocol": protocol_num}
                save_json_file(PROTOCOL_FILE, protocol_data)
                replyMsg(plugin_event, f"已设置使用协议 {protocol_num}")
            else:
                replyMsg(plugin_event, "协议序号无效，请输入1、2或3")
        except ValueError:
            replyMsg(plugin_event, "请输入有效的协议序号(1、2或3)")
        return True
    
    # 添加白名单群组
    if isMatchWordStart(tmp_reast_str, ['回应添加白名单群组'], isCommand=True):
        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['回应添加白名单群组'])
        tmp_reast_str = skipSpaceStart(tmp_reast_str)
        group_id = tmp_reast_str.strip()
        
        if group_id and group_id not in whitelist["whitelist_groups"]:
            whitelist["whitelist_groups"].append(group_id)
            save_json_file(WHITELIST_FILE, whitelist)
            replyMsg(plugin_event, f"已添加群组 {group_id} 到白名单")
        else:
            replyMsg(plugin_event, "群组ID无效或已在白名单中")
        return True
    
    # 移除白名单群组
    if isMatchWordStart(tmp_reast_str, ['回应移除白名单群组'], isCommand=True):
        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['回应移除白名单群组'])
        tmp_reast_str = skipSpaceStart(tmp_reast_str)
        group_id = tmp_reast_str.strip()
        
        if group_id and group_id in whitelist["whitelist_groups"]:
            whitelist["whitelist_groups"].remove(group_id)
            save_json_file(WHITELIST_FILE, whitelist)
            replyMsg(plugin_event, f"已从白名单移除群组 {group_id}")
        else:
            replyMsg(plugin_event, "群组ID无效或不在白名单中")
        return True
    
    # 添加目标用户
    if isMatchWordStart(tmp_reast_str, ['回应添加用户'], isCommand=True):
        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['回应添加用户'])
        tmp_reast_str = skipSpaceStart(tmp_reast_str)
        parts = tmp_reast_str.split(maxsplit=1)
        
        if len(parts) >= 2:
            qq_id = parts[0].strip()
            emojis = parts[1].strip().split()
            
            if qq_id and emojis:
                config["target_users"][qq_id] = emojis
                save_json_file(CONFIG_FILE, config)
                replyMsg(plugin_event, f"已为用户 {qq_id} 添加表情: {' '.join(emojis)}")
            else:
                replyMsg(plugin_event, "命令格式错误，应为: 回应添加用户 QQ号 表情1 表情2 ...")
        else:
            replyMsg(plugin_event, "命令格式错误，应为: 回应添加用户 QQ号 表情1 表情2 ...")
        return True
    
    # 移除目标用户
    if isMatchWordStart(tmp_reast_str, ['回应移除用户'], isCommand=True):
        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['回应移除用户'])
        tmp_reast_str = skipSpaceStart(tmp_reast_str)
        qq_id = tmp_reast_str.strip()
        
        if qq_id and qq_id in config["target_users"]:
            del config["target_users"][qq_id]
            save_json_file(CONFIG_FILE, config)
            replyMsg(plugin_event, f"已移除目标用户 {qq_id}")
        else:
            replyMsg(plugin_event, "用户ID无效或不是目标用户")
        return True
    
    # 为用户添加表情
    if isMatchWordStart(tmp_reast_str, ['回应添加表情'], isCommand=True):
        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['回应添加表情'])
        tmp_reast_str = skipSpaceStart(tmp_reast_str)
        parts = tmp_reast_str.split(maxsplit=1)
        
        if len(parts) >= 2:
            qq_id = parts[0].strip()
            emojis = parts[1].strip().split()
            
            if qq_id and emojis and qq_id in config["target_users"]:
                config["target_users"][qq_id].extend(emojis)
                save_json_file(CONFIG_FILE, config)
                replyMsg(plugin_event, f"已为用户 {qq_id} 添加表情: {' '.join(emojis)}")
            else:
                replyMsg(plugin_event, "用户ID无效或不是目标用户")
        else:
            replyMsg(plugin_event, "命令格式错误，应为: 回应添加表情 QQ号 表情1 表情2 ...")
        return True
    
    # 为用户移除表情
    if isMatchWordStart(tmp_reast_str, ['回应移除表情'], isCommand=True):
        tmp_reast_str = getMatchWordStartRight(tmp_reast_str, ['回应移除表情'])
        tmp_reast_str = skipSpaceStart(tmp_reast_str)
        parts = tmp_reast_str.split(maxsplit=1)
        
        if len(parts) >= 2:
            qq_id = parts[0].strip()
            emojis = parts[1].strip().split()
            
            if qq_id and emojis and qq_id in config["target_users"]:
                for emoji in emojis:
                    if emoji in config["target_users"][qq_id]:
                        config["target_users"][qq_id].remove(emoji)
                save_json_file(CONFIG_FILE, config)
                replyMsg(plugin_event, f"已为用户 {qq_id} 移除表情: {' '.join(emojis)}")
            else:
                replyMsg(plugin_event, "用户ID无效或不是目标用户")
        else:
            replyMsg(plugin_event, "命令格式错误，应为: 回应移除表情 QQ号 表情1 表情2 ...")
        return True
    
    # 查看当前配置
    if isMatchWordStart(tmp_reast_str, ['回应查看配置'], isCommand=True):
        whitelist_groups = "\n".join(whitelist["whitelist_groups"]) or "无"
        target_users = "\n".join([f"{k}: {' '.join(v)}" for k, v in config["target_users"].items()]) or "无"
        current_protocol = get_protocol()
        
        replyMsg(plugin_event, 
            f"白名单群组:\n{whitelist_groups}\n\n"
            f"目标用户及表情:\n{target_users}\n\n"
            f"当前使用的协议: {current_protocol}\n"
            f"(1：Lagrange, 2：NapCat, 3：LLOneBot/LLTwoBot)"
        )
        return True
    
    return False

def unity_reply(plugin_event, Proc):
    # 初始化消息处理
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

    def is_master(plugin_event):
        """检查是否是骰骰主"""
        return OlivaDiceCore.ordinaryInviteManager.isInMasterList(
            plugin_event.bot_info.hash,
            OlivaDiceCore.userConfig.getUserHash(
                plugin_event.data.user_id,
                'user',
                plugin_event.platform['platform']
            )
        )
    
    # 处理骰骰主命令
    if flag_is_command and is_master(plugin_event):
        if handle_admin_command(plugin_event, dictTValue, dictStrCustom, tmp_reast_str):
            plugin_event.set_block()
            return
    
    # 检查是否是群消息
    if plugin_event.plugin_info['func_type'] == 'group_message':
        # 加载配置
        config = load_json_file(CONFIG_FILE)
        whitelist = load_json_file(WHITELIST_FILE)
        
        # 检查是否在白名单群组中
        group_id = str(plugin_event.data.group_id)
        if "whitelist_groups" in whitelist and group_id not in whitelist["whitelist_groups"]:
            return
        
        # 获取发送者QQ号
        sender_id = str(plugin_event.data.user_id)
        
        # 检查是否是目标用户
        if "target_users" in config and sender_id in config["target_users"]:
            # 获取账号配置
            server_config = get_account_config(plugin_event)
            if server_config is None:
                replyMsg(plugin_event, "无法读取账号配置，请检查 conf/account.json 文件")
                return
                
            # 发送表情回应
            reaction_codes = config["target_users"][sender_id]
            message_id = plugin_event.data.message_id
            
            if not send_reactions(plugin_event, server_config, message_id, reaction_codes):
                replyMsg(plugin_event, f"检测到目标用户 {sender_id}，但表情回应发送失败")