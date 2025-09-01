import OlivOS
import OlivaDiceCore
import json
import os
import re

# 全局定义数据存储路径
data_path = "plugin/data/SmartInterceptor"

# 用法回复
interception_used_str = '''拦截词支持三种匹配模式：
1. 完全匹配：直接输入要拦截的词 (如：work)
2. 前缀匹配：在词后加 * (如：work* 会拦截 work 开头的词，如 work123)
3. 正则匹配：用 / 包围正则表达式 (如：/^work.*$/ 会拦截 work 开头的词)
'''

class Event(object):
    # 命令
    COMMAND_PREFIX = "添加拦截词"
    REMOVE_PREFIX = "删除拦截词"
    LIST_PREFIX = "查看拦截词"
    TOGGLE_PREFIX = "开关拦截词"
    TOGGLE_ON = "开启"
    TOGGLE_OFF = "关闭"
    TOGGLE_STATUS = "状态"
    GLOBAL_SCOPE = "全局"
    GROUP_SCOPE = "群"
    
    @classmethod
    def init(cls, plugin_event, Proc):
        # 确保数据目录存在
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        
        # 全局拦截词文件
        global_words_file = os.path.join(data_path, "global_words.json")
        # 分群拦截词文件
        group_words_file = os.path.join(data_path, "group_words.json")
        # 拦截功能开关状态文件
        toggle_status_file = os.path.join(data_path, "toggle_status.json")
        
        # 初始化文件
        if not os.path.exists(global_words_file):
            with open(global_words_file, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)
            Proc.log(2, "[SmartInterceptor] 已创建全局拦截词文件")
        
        if not os.path.exists(group_words_file):
            with open(group_words_file, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=4)
            Proc.log(2, "[SmartInterceptor] 已创建分群拦截词文件")
        
        if not os.path.exists(toggle_status_file):
            with open(toggle_status_file, "w", encoding="utf-8") as f:
                json.dump({
                    "global": True,
                    "global_groups": {},
                    "group_groups": {}
                }, f, indent=4)
            Proc.log(2, "[SmartInterceptor] 已创建拦截功能开关状态文件")

    @classmethod
    def is_dice_master(cls, plugin_event):
        """骰主检查方法"""
        if not hasattr(plugin_event.data, 'user_id'):
            return False
            
        # 使用OlivaDiceCore的master列表检查
        user_hash = OlivaDiceCore.userConfig.getUserHash(
            plugin_event.data.user_id,
            'user',
            plugin_event.platform['platform']
        )
        return OlivaDiceCore.ordinaryInviteManager.isInMasterList(
            plugin_event.bot_info.hash,
            user_hash
        )

    @classmethod
    def is_group_admin_or_owner(cls, plugin_event):
        """群管理检查方法"""
        if not hasattr(plugin_event.data, 'group_id'):
            return False
            
        # 检查发送者角色
        sender = getattr(plugin_event.data, 'sender', {})
        role = sender.get('role', '')
        return role in ['owner', 'admin', 'sub_admin']

    @classmethod
    def has_permission(cls, plugin_event, scope):
        """
        权限检查方法
        scope: 'global' 或 'group'
        """
        if scope == 'global':
            return cls.is_dice_master(plugin_event)
        elif scope == 'group':
            return cls.is_dice_master(plugin_event) or cls.is_group_admin_or_owner(plugin_event)
        return False

    @classmethod
    def private_message(cls, plugin_event, Proc):
        # 私聊只处理全局拦截词相关命令
        cls.handle_private_message(plugin_event, Proc)

    @classmethod
    def group_message(cls, plugin_event, Proc):
        # 群聊处理所有命令
        cls.handle_group_message(plugin_event, Proc)

    @classmethod
    def handle_private_message(cls, plugin_event, Proc):
        """处理私聊消息 - 只处理全局拦截词相关命令"""
        try:
            # 文件路径
            global_words_file = os.path.join(data_path, "global_words.json")
            
            # 读取全局拦截词
            with open(global_words_file, "r", encoding="utf-8") as f:
                global_words = json.load(f)
            
            raw_msg = plugin_event.data.message.strip()
            
            # 处理添加全局拦截词命令
            if raw_msg.startswith(cls.COMMAND_PREFIX):
                parts = raw_msg[len(cls.COMMAND_PREFIX):].strip().split(maxsplit=1)
                if len(parts) == 2:
                    scope, word = parts
                    if scope == cls.GLOBAL_SCOPE:
                        if not cls.is_dice_master(plugin_event):
                            return
                            
                        # 检查是否已存在相似模式
                        existing = next((w for w in global_words if cls.is_match(word, w)), None)
                        if existing:
                            plugin_event.reply(f"全局拦截词 [{word}] 与现有拦截词 [{existing}] 冲突")
                            return
                            
                        global_words.append(word)
                        with open(global_words_file, "w", encoding="utf-8") as f:
                            json.dump(global_words, f, indent=4)
                            
                        Proc.log(2, f"[SmartInterceptor] 骰主 {plugin_event.data.user_id} 添加全局拦截词：{word}")
                        plugin_event.reply(f"已添加全局拦截词: {word}")
                    else:
                        plugin_event.reply("私聊只能配置全局拦截词")
                else:
                    plugin_event.reply(
                        f"用法: {cls.COMMAND_PREFIX} [{cls.GLOBAL_SCOPE}|{cls.GROUP_SCOPE}] [拦截词]\n"

                    )
                return
                
            # 处理删除全局拦截词命令
            if raw_msg.startswith(cls.REMOVE_PREFIX):
                parts = raw_msg[len(cls.REMOVE_PREFIX):].strip().split(maxsplit=1)
                if len(parts) == 2:
                    scope, word = parts
                    if scope == cls.GLOBAL_SCOPE:
                        if not cls.is_dice_master(plugin_event):
                            return
                            
                        if word in global_words:
                            global_words.remove(word)
                            with open(global_words_file, "w", encoding="utf-8") as f:
                                json.dump(global_words, f, indent=4)
                                
                            Proc.log(2, f"[SmartInterceptor] 骰主 {plugin_event.data.user_id} 删除全局拦截词：{word}")
                            plugin_event.reply(f"已删除全局拦截词: {word}")
                        else:
                            plugin_event.reply(f"全局拦截词 [{word}] 不存在")
                    else:
                        plugin_event.reply("私聊只能配置全局拦截词")
                else:
                    plugin_event.reply(
                        f"用法: {cls.REMOVE_PREFIX} [{cls.GLOBAL_SCOPE}|{cls.GROUP_SCOPE}] [拦截词]\n" + interception_used_str
                    )
                return
                
            # 处理全局拦截功能开关命令
            if raw_msg.startswith(cls.TOGGLE_PREFIX):
                parts = raw_msg[len(cls.TOGGLE_PREFIX):].strip().split()
                if len(parts) >= 1:
                    # 私聊只能处理全局总开关
                    if len(parts) == 1:
                        action = parts[0]
                        if action not in [cls.TOGGLE_ON, cls.TOGGLE_OFF]:
                            plugin_event.reply(f"用法: {cls.TOGGLE_PREFIX} [{cls.TOGGLE_ON}|{cls.TOGGLE_OFF}]")
                            return
                            
                        if not cls.is_dice_master(plugin_event):
                            return
                            
                        toggle_status = cls.get_toggle_status()
                        new_status = action == cls.TOGGLE_ON
                        toggle_status["global"] = new_status
                        cls.set_toggle_status(toggle_status)
                        
                        status_str = cls.TOGGLE_ON if new_status else cls.TOGGLE_OFF
                        Proc.log(2, f"[SmartInterceptor] 骰主 {plugin_event.data.user_id} {status_str}全局拦截功能")
                        plugin_event.reply(f"已{status_str}全局拦截功能")
                    else:
                        plugin_event.reply("私聊只能配置全局拦截总开关")
                return
                
            # 处理查看全局拦截词命令
            if raw_msg.startswith(cls.LIST_PREFIX):
                parts = raw_msg[len(cls.LIST_PREFIX):].strip().split()
                scope = parts[0] if parts else None
                
                if scope == cls.GLOBAL_SCOPE:
                    if not cls.is_dice_master(plugin_event):
                        return
                        
                    if global_words:
                        plugin_event.reply("全局拦截词列表:\n" + "\n".join(global_words))
                    else:
                        plugin_event.reply("当前没有全局拦截词")
                else:
                    plugin_event.reply(f"用法: {cls.LIST_PREFIX} {cls.GLOBAL_SCOPE}")
                return
                
        except json.JSONDecodeError:
            Proc.log(4, "[SmartInterceptor] 配置文件损坏，正在重置")
            cls.init(plugin_event, Proc)
            plugin_event.reply("配置文件损坏，已重置为默认配置")
            
        except Exception as e:
            Proc.log(4, f"[SmartInterceptor] 处理私聊消息时出错: {str(e)}")
            plugin_event.reply("处理命令时发生错误")

    @classmethod
    def handle_group_message(cls, plugin_event, Proc):
        """处理群聊消息 - 处理所有命令"""
        try:
            # 文件路径
            global_words_file = os.path.join(data_path, "global_words.json")
            group_words_file = os.path.join(data_path, "group_words.json")
            
            # 读取数据
            with open(global_words_file, "r", encoding="utf-8") as f:
                global_words = json.load(f)
            
            with open(group_words_file, "r", encoding="utf-8") as f:
                group_words = json.load(f)
            
            toggle_status = cls.get_toggle_status()
            
            raw_msg = plugin_event.data.message.strip()
            user_id = str(plugin_event.data.user_id)
            group_id = str(plugin_event.data.group_id)
            
            # 处理添加命令
            if raw_msg.startswith(cls.COMMAND_PREFIX):
                parts = raw_msg[len(cls.COMMAND_PREFIX):].strip().split(maxsplit=1)
                if len(parts) == 2:
                    scope, word = parts
                    if scope == cls.GLOBAL_SCOPE:
                        if not cls.is_dice_master(plugin_event):
                            plugin_event.reply("权限不足：只有骰主可以修改全局拦截词")
                            return
                            
                        # 检查是否已存在相似模式
                        existing = next((w for w in global_words if cls.is_match(word, w)), None)
                        if existing:
                            plugin_event.reply(f"全局拦截词 [{word}] 与现有拦截词 [{existing}] 冲突")
                            return
                            
                        global_words.append(word)
                        with open(global_words_file, "w", encoding="utf-8") as f:
                            json.dump(global_words, f, indent=4)
                            
                        Proc.log(2, f"[SmartInterceptor] 骰主 {user_id} 添加全局拦截词：{word}")
                        plugin_event.reply(f"已添加全局拦截词: {word}")
                        
                    elif scope == cls.GROUP_SCOPE:
                        if not cls.has_permission(plugin_event, 'group'):
                            plugin_event.reply("权限不足：只有骰主或本群管理员可以修改群拦截词")
                            return
                            
                        if group_id not in group_words:
                            group_words[group_id] = []
                            
                        # 检查是否已存在相似模式
                        existing = next((w for w in group_words.get(group_id, []) if cls.is_match(word, w)), None)
                        if existing:
                            plugin_event.reply(f"本群拦截词 [{word}] 与现有拦截词 [{existing}] 冲突")
                            return
                            
                        group_words[group_id].append(word)
                        with open(group_words_file, "w", encoding="utf-8") as f:
                            json.dump(group_words, f, indent=4)
                            
                        Proc.log(2, f"[SmartInterceptor] 用户 {user_id} 添加群 {group_id} 拦截词：{word}")
                        plugin_event.reply(f"已添加本群拦截词: {word}")
                    else:
                        plugin_event.reply(f"无效的作用域，请使用 {cls.GLOBAL_SCOPE} 或 {cls.GROUP_SCOPE}")
                else:
                    plugin_event.reply(
                        f"用法: {cls.COMMAND_PREFIX} [{cls.GLOBAL_SCOPE}|{cls.GROUP_SCOPE}] [拦截词]\n" + interception_used_str
                    )
                return
                
            # 处理删除命令
            if raw_msg.startswith(cls.REMOVE_PREFIX):
                parts = raw_msg[len(cls.REMOVE_PREFIX):].strip().split(maxsplit=1)
                if len(parts) == 2:
                    scope, word = parts
                    if scope == cls.GLOBAL_SCOPE:
                        if not cls.is_dice_master(plugin_event):
                            plugin_event.reply("权限不足：只有骰主可以修改全局拦截词")
                            return
                            
                        if word in global_words:
                            global_words.remove(word)
                            with open(global_words_file, "w", encoding="utf-8") as f:
                                json.dump(global_words, f, indent=4)
                                
                            Proc.log(2, f"[SmartInterceptor] 骰主 {user_id} 删除全局拦截词：{word}")
                            plugin_event.reply(f"已删除全局拦截词: {word}")
                        else:
                            plugin_event.reply(f"全局拦截词 [{word}] 不存在")
                            
                    elif scope == cls.GROUP_SCOPE:
                        if not cls.has_permission(plugin_event, 'group'):
                            plugin_event.reply("权限不足：只有骰主或本群管理员可以修改群拦截词")
                            return
                            
                        if group_id in group_words and word in group_words[group_id]:
                            group_words[group_id].remove(word)
                            with open(group_words_file, "w", encoding="utf-8") as f:
                                json.dump(group_words, f, indent=4)
                                
                            Proc.log(2, f"[SmartInterceptor] 用户 {user_id} 删除群 {group_id} 拦截词：{word}")
                            plugin_event.reply(f"已删除本群拦截词: {word}")
                        else:
                            plugin_event.reply(f"本群拦截词 [{word}] 不存在")
                    else:
                        plugin_event.reply(f"无效的作用域，请使用 {cls.GLOBAL_SCOPE} 或 {cls.GROUP_SCOPE}")
                else:
                    plugin_event.reply(
                        f"用法: {cls.REMOVE_PREFIX} [{cls.GLOBAL_SCOPE}|{cls.GROUP_SCOPE}] [拦截词]\n" + interception_used_str
                    )
                return
                
            # 处理查看命令 - 只在群聊中可用
            if raw_msg.startswith(cls.LIST_PREFIX):
                parts = raw_msg[len(cls.LIST_PREFIX):].strip().split()
                scope = parts[0] if parts else None
                
                if scope == cls.GLOBAL_SCOPE:
                    if not cls.is_dice_master(plugin_event):
                        plugin_event.reply("权限不足：只有骰主可以查看全局拦截词列表")
                        return
                        
                    if global_words:
                        plugin_event.reply("全局拦截词列表:\n" + "\n".join(global_words))
                    else:
                        plugin_event.reply("当前没有全局拦截词")
                elif scope == cls.GROUP_SCOPE:
                    if group_id in group_words and group_words[group_id]:
                        plugin_event.reply(f"本群拦截词列表:\n" + "\n".join(group_words[group_id]))
                    else:
                        plugin_event.reply("本群没有设置拦截词")
                else:
                    plugin_event.reply(f"用法: {cls.LIST_PREFIX} [{cls.GLOBAL_SCOPE}|{cls.GROUP_SCOPE}]")
                return
                
            # 处理拦截功能开关命令
            if raw_msg.startswith(cls.TOGGLE_PREFIX):
                parts = raw_msg[len(cls.TOGGLE_PREFIX):].strip().split()
                
                # 状态查询功能
                if len(parts) >= 1 and parts[-1] == cls.TOGGLE_STATUS:
                    global_status = cls.TOGGLE_ON if toggle_status["global"] else cls.TOGGLE_OFF
                    global_group_status = cls.TOGGLE_ON if toggle_status["global_groups"].get(group_id, True) else cls.TOGGLE_OFF
                    group_group_status = cls.TOGGLE_ON if toggle_status["group_groups"].get(group_id, True) else cls.TOGGLE_OFF
                    
                    reply_msg = (
                        "当前拦截功能状态:\n"
                        f"全局拦截总开关: {global_status}\n"
                        f"本群全局拦截开关: {global_group_status}\n"
                        f"本群群拦截开关: {group_group_status}"
                    )
                    plugin_event.reply(reply_msg)
                    return
                
                # 处理开关命令
                if len(parts) == 1:
                    # 全局总开关
                    action = parts[0]
                    if action not in [cls.TOGGLE_ON, cls.TOGGLE_OFF]:
                        plugin_event.reply(f"用法: {cls.TOGGLE_PREFIX} [{cls.TOGGLE_ON}|{cls.TOGGLE_OFF}] (全局总开关)")
                        return
                        
                    if not cls.is_dice_master(plugin_event):
                        plugin_event.reply("权限不足：只有骰主可以修改全局拦截总开关")
                        return
                        
                    new_status = action == cls.TOGGLE_ON
                    toggle_status["global"] = new_status
                    cls.set_toggle_status(toggle_status)
                    
                    status_str = cls.TOGGLE_ON if new_status else cls.TOGGLE_OFF
                    Proc.log(2, f"[SmartInterceptor] 骰主 {user_id} {status_str}全局拦截总开关")
                    plugin_event.reply(f"已{status_str}全局拦截总开关")
                    
                elif len(parts) == 2:
                    # 群内开关
                    scope, action = parts
                    
                    if scope == cls.GLOBAL_SCOPE:
                        # 本群全局拦截开关
                        if action not in [cls.TOGGLE_ON, cls.TOGGLE_OFF]:
                            plugin_event.reply(f"用法: {cls.TOGGLE_PREFIX} {cls.GLOBAL_SCOPE} [{cls.TOGGLE_ON}|{cls.TOGGLE_OFF}]")
                            return
                            
                        if not cls.has_permission(plugin_event, 'group'):
                            plugin_event.reply("权限不足：只有骰主或本群管理员可以修改本群全局拦截开关")
                            return
                            
                        new_status = action == cls.TOGGLE_ON
                        toggle_status["global_groups"][group_id] = new_status
                        cls.set_toggle_status(toggle_status)
                        
                        status_str = cls.TOGGLE_ON if new_status else cls.TOGGLE_OFF
                        Proc.log(2, f"[SmartInterceptor] 用户 {user_id} {status_str}群 {group_id} 全局拦截开关")
                        plugin_event.reply(f"已{status_str}本群全局拦截开关")
                        
                    elif scope == cls.GROUP_SCOPE:
                        # 本群群拦截开关
                        if action not in [cls.TOGGLE_ON, cls.TOGGLE_OFF]:
                            plugin_event.reply(f"用法: {cls.TOGGLE_PREFIX} {cls.GROUP_SCOPE} [{cls.TOGGLE_ON}|{cls.TOGGLE_OFF}]")
                            return
                            
                        if not cls.has_permission(plugin_event, 'group'):
                            plugin_event.reply("权限不足：只有骰主或本群管理员可以修改本群群拦截开关")
                            return
                            
                        new_status = action == cls.TOGGLE_ON
                        toggle_status["group_groups"][group_id] = new_status
                        cls.set_toggle_status(toggle_status)
                        
                        status_str = cls.TOGGLE_ON if new_status else cls.TOGGLE_OFF
                        Proc.log(2, f"[SmartInterceptor] 用户 {user_id} {status_str}群 {group_id} 群拦截开关")
                        plugin_event.reply(f"已{status_str}本群群拦截开关")
                    
                    else:
                        plugin_event.reply(f"用法: {cls.TOGGLE_PREFIX} [{cls.GLOBAL_SCOPE}|{cls.GROUP_SCOPE}] [{cls.TOGGLE_ON}|{cls.TOGGLE_OFF}]")
                else:
                    plugin_event.reply(f"用法: {cls.TOGGLE_PREFIX} [{cls.TOGGLE_ON}|{cls.TOGGLE_OFF}] (全局总开关)\n"
                                     f"或 {cls.TOGGLE_PREFIX} [{cls.GLOBAL_SCOPE}|{cls.GROUP_SCOPE}] [{cls.TOGGLE_ON}|{cls.TOGGLE_OFF}]")
                return

            # 拦截检查
            # 1. 检查全局拦截总开关是否开启
            if toggle_status["global"]:
                # 2. 检查本群全局拦截开关是否开启（默认开启）
                if toggle_status["global_groups"].get(group_id, True):
                    matched = next((p for p in global_words if cls.is_match(raw_msg, p)), None)
                    if matched:
                        Proc.log(2, f"[SmartInterceptor] 已拦截全局指令：{raw_msg} (匹配模式: {matched})")
                        plugin_event.set_block()
                        return
                
            # 3. 检查本群群拦截开关是否开启（默认开启）
            if toggle_status["group_groups"].get(group_id, True):
                if group_id in group_words:
                    matched = next((p for p in group_words[group_id] if cls.is_match(raw_msg, p)), None)
                    if matched:
                        Proc.log(2, f"[SmartInterceptor] 已拦截群 {group_id} 指令：{raw_msg} (匹配模式: {matched})")
                        plugin_event.set_block()
                
        except json.JSONDecodeError:
            Proc.log(4, "[SmartInterceptor] 配置文件损坏，正在重置")
            cls.init(plugin_event, Proc)
            plugin_event.reply("配置文件损坏，已重置为默认配置")
            
        except Exception as e:
            Proc.log(4, f"[SmartInterceptor] 处理群聊消息时出错: {str(e)}")
            plugin_event.reply("处理命令时发生错误")

    @classmethod
    def is_match(cls, message, pattern):
        """正则表达式匹配"""
        try:
            if pattern.startswith('/') and pattern.endswith('/'):
                # 正则表达式模式 (如 "/^work.*$/")
                regex_pattern = pattern[1:-1]
                return re.search(regex_pattern, message) is not None
            elif pattern.endswith('*'):
                # 开头匹配模式 (如 "work*" 匹配 "work123")
                return message.startswith(pattern[:-1])
            else:
                # 完全匹配模式
                return message == pattern
        except re.error:
            return message == pattern

    @classmethod
    def get_toggle_status(cls):
        """获取拦截功能开关状态"""
        toggle_status_file = os.path.join(data_path, "toggle_status.json")
        try:
            with open(toggle_status_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"global": True, "global_groups": {}, "group_groups": {}}

    @classmethod
    def set_toggle_status(cls, status):
        """设置拦截功能开关状态"""
        toggle_status_file = os.path.join(data_path, "toggle_status.json")
        with open(toggle_status_file, "w", encoding="utf-8") as f:
            json.dump(status, f, indent=4)