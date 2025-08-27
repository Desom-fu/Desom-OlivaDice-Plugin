import OlivOS
import OlivaDiceCore
import json
import os
import re
import random
try:
    # 导入pypinyin
    from pypinyin import lazy_pinyin, Style
    PINYIN_SUPPORT = True
except ImportError:
    # 如果导入失败，就无法拼音模糊搜索
    PINYIN_SUPPORT = False

data_path = "plugin/data/LexNinjutsu"

class Event(object):
    COMMAND_ADD = ["添加忍术", "增加忍术", "增添忍术"]
    COMMAND_DEL = "删除忍术"
    COMMAND_CAST = "释放忍术"
    COMMAND_MANAGE = "管理忍术"
    COMMAND_LIST = ["查看忍术", "忍术列表", "列出忍术", "忍术查看", "忍术查询", "查询忍术"]
    COMMAND_RANDOM = ["随机忍术", "随机释放", "忍术随机"]
    COMMAND_HELP = ["忍术帮助", "帮助忍术", "ninjutsu help"]
    COMMAND_ADD_ALIAS = ["添加别名", "增加别名"]
    COMMAND_DEL_ALIAS = ["删除别名", "移除别名"]
    COMMAND_QUERY_ALIAS = ["查询别名", "查看别名", "别名查询"]
    COMMAND_UPDATE = ["修改忍术", "更改忍术", "更新忍术"]
    NINJUTSU_LEVELS = ["E", "D", "C", "B", "A", "S", "禁术"]  # 忍术等级分类
    
    @classmethod
    def init(cls, plugin_event, Proc):
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        
        # 初始化全局文件结构
        for fname in ["ninjutsu.json", "permissions.json", "aliases.json"]:
            fpath = os.path.join(data_path, fname)
            if not os.path.exists(fpath):
                if fname == "ninjutsu.json":
                    default = {level: {} for level in cls.NINJUTSU_LEVELS}
                elif fname == "aliases.json":
                    default = {}
                else:
                    default = {"admin": [], "manager": []}
                with open(fpath, "w", encoding="utf-8") as f:
                    json.dump(default, f, indent=4)
                Proc.log(2, f"[LexNinjutsu] 已初始化 {fname}")

    # region 权限系统
    @classmethod
    def is_dice_master(cls, plugin_event):
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
    def is_group_owner_or_admin(cls, plugin_event):
        sender = getattr(plugin_event.data, 'sender', {})
        return sender.get('role') in ['owner', 'admin']

    @classmethod
    def check_permission(cls, plugin_event, require_level):
        """
        权限层级：骰主 > admin > manager(群管/群主)
        require_level: 'admin' 或 'manager'
        """
        if cls.is_dice_master(plugin_event):
            return True
            
        with open(os.path.join(data_path, "permissions.json"), "r") as f:
            perms = json.load(f)
        
        if require_level == 'admin':
            return str(plugin_event.data.user_id) in perms.get('admin', [])
            
        if require_level == 'manager':
            # 群主/管理员自动获得权限
            return (cls.is_group_owner_or_admin(plugin_event) or 
                    str(plugin_event.data.user_id) in perms.get('manager', []))
        return False

    @classmethod
    def check_permission_exists(cls, user_id):
        """检查用户是否已有任何权限"""
        with open(os.path.join(data_path, "permissions.json"), "r") as f:
            perms = json.load(f)
        user_id = str(user_id)
        return (user_id in perms.get('admin', []) or 
                user_id in perms.get('manager', []))
    # endregion

    # region 别名功能
    @classmethod
    def get_original_name(cls, alias):
        """通过别名获取原名"""
        alias_path = os.path.join(data_path, "aliases.json")
        if not os.path.exists(alias_path):
            return None
            
        with open(alias_path, "r", encoding="utf-8") as f:
            aliases = json.load(f)
            return aliases.get(alias.upper(), None)

    @classmethod
    def add_alias(cls, original_name, alias_name):
        """添加别名"""
        alias_path = os.path.join(data_path, "aliases.json")
        
        # 检查原名是否存在
        with open(os.path.join(data_path, "ninjutsu.json"), "r", encoding="utf-8") as f:
            ninjutsu = json.load(f)
            exists = False
            for level in cls.NINJUTSU_LEVELS:
                if original_name.upper() in ninjutsu[level]:
                    exists = True
                    break
            if not exists:
                return False, "忍术原名不存在，请先添加忍术"
        
        # 检查别名是否与原名相同
        if alias_name.upper() == original_name.upper():
            return False, "别名不能与原名相同"
            
        # 检查别名是否已被使用
        original = cls.get_original_name(alias_name)
        if original is not None:
            return False, "该别名已被使用"
            
        # 检查别名是否与现有忍术名冲突
        with open(os.path.join(data_path, "ninjutsu.json"), "r", encoding="utf-8") as f:
            ninjutsu = json.load(f)
            for level in cls.NINJUTSU_LEVELS:
                if alias_name.upper() in ninjutsu[level]:
                    return False, "该别名与现有忍术名称冲突"
            
        # 添加别名
        with open(alias_path, "r+", encoding="utf-8") as f:
            aliases = json.load(f)
            aliases[alias_name.upper()] = original_name.upper()
            f.seek(0)
            json.dump(aliases, f, indent=4, ensure_ascii=False)
            f.truncate()
            
        return True, f"已为忍术 [{original_name}] 添加别名 [{alias_name}]"

    @classmethod
    def remove_alias(cls, alias_name):
        """删除别名"""
        alias_path = os.path.join(data_path, "aliases.json")
        
        with open(alias_path, "r+", encoding="utf-8") as f:
            aliases = json.load(f)
            if alias_name.upper() not in aliases:
                return False, "别名不存在"
                
            original_name = aliases[alias_name.upper()]
            del aliases[alias_name.upper()]
            f.seek(0)
            json.dump(aliases, f, indent=4, ensure_ascii=False)
            f.truncate()
            
        return True, f"已删除忍术 [{original_name}] 的别名 [{alias_name}]"
    # endregion

    # region 忍术核心功能
    @classmethod
    def match_by_pinyin(cls, input_str, ninjutsu_data):
        # 拼音模糊匹配
        if not PINYIN_SUPPORT:
            return None, 0, None

        # 提取开头的英文字母部分（纯拼音）
        match = re.match(r'^[a-zA-Z]+', input_str)
        if not match:
            return None, 0, None

        pinyin_part = match.group(0)
        input_lower = pinyin_part.lower()
        input_pinyin = ''.join(lazy_pinyin(input_lower, style=Style.NORMAL))
        input_initials = ''.join(lazy_pinyin(input_lower, style=Style.FIRST_LETTER))

        # 在所有忍术中查找拼音匹配
        best_match = None
        best_length = 0
        match_type = None

        # 检查所有忍术等级
        for level in cls.NINJUTSU_LEVELS:
            for name in ninjutsu_data[level].keys():
                # 获取忍术名称的拼音形式
                name_lower = name.lower()
                name_pinyin = ''.join(lazy_pinyin(name_lower, style=Style.NORMAL))
                name_initials = ''.join(lazy_pinyin(name_lower, style=Style.FIRST_LETTER))

                # 1. 全拼完全匹配
                if input_pinyin and input_pinyin == name_pinyin:
                    if len(name) > best_length:
                        best_match = name
                        best_length = len(name)
                        match_type = "全拼匹配"
                        continue
                    
                # 2. 首字母完全匹配
                if input_initials and input_initials == name_initials:
                    if len(name) > best_length:
                        best_match = name
                        best_length = len(name)
                        match_type = "首字母匹配"

                # 3. 部分拼音匹配
                if input_pinyin and name_pinyin.startswith(input_pinyin):
                    if len(input_pinyin) > best_length:
                        best_match = name
                        best_length = len(input_pinyin)
                        match_type = "部分拼音匹配"

        # 如果找到匹配，返回匹配结果
        if best_match:
            return best_match, len(pinyin_part), match_type
        return None, 0, None

    @classmethod
    def save_ninjutsu(cls, name, level, expression):
        # 检查是否是别名
        alias_path = os.path.join(data_path, "aliases.json")
        if os.path.exists(alias_path):
            with open(alias_path, "r", encoding="utf-8") as f:
                aliases = json.load(f)
                if name.strip().upper() in aliases:
                    return False  # 名称与现有别名冲突

        with open(os.path.join(data_path, "ninjutsu.json"), "r+") as f:
            data = json.load(f)
            # 检查所有等级中是否已存在同名忍术
            for lvl in cls.NINJUTSU_LEVELS:
                if name.strip() in data[lvl]:
                    return False  # 忍术已存在

            if level not in cls.NINJUTSU_LEVELS:
                level = "E"  # 默认等级为E

            data[level][name.strip()] = expression.strip()
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.truncate()
        return True

    @classmethod
    def get_pc_attribute(cls, user_id, platform, attr, group_id=None):
        pc_hash = OlivaDiceCore.pcCard.getPcHash(user_id, platform)
        # 如果有群组ID，使用群组ID获取锁定人物卡的属性
        if group_id is not None:
            value = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(
                pc_hash, 
                attr, 
                hagId=group_id
            )
        else:
            value = OlivaDiceCore.pcCard.pcCardDataGetBySkillName(pc_hash, attr)
        return value if value is not None else 0

    @classmethod
    def parse_attributes(cls, remaining, user_id, platform, Proc, group_id=None):
        """解析属性覆盖表达式，支持连续属性和骰子表达式"""
        overrides = {}
        override_details = []
        invalid_parts = []
        base_overrides = {}  # 记录原始属性值
        consumed = ""

        # 解析状态
        while remaining:
            # 1. 匹配属性名 (中文字符或英文字母开头)
            match = re.search(r'^([\u4e00-\u9fa5a-zA-Z]+)', remaining)
            if not match:
                # 没有属性名，结束解析
                invalid_parts.append(remaining)
                break
            
            attr = match.group(1).upper()
            consumed += match.group(0)
            remaining = remaining[len(match.group(0)):].lstrip()

            # 2. 匹配运算符 (=、+、-、*、/)
            op = None
            if remaining and remaining[0] in ('=', '+', '-', '*', '/'):
                op = remaining[0]
                consumed += op
                remaining = remaining[1:].lstrip()
            elif remaining and remaining.startswith('-'):
                # 处理负号运算符
                op = '-'
                consumed += '-'
                remaining = remaining[1:].lstrip()

            # 3. 匹配表达式部分 - 更智能的表达式解析
            expr_str = ""
            in_dice = False  # 标记是否在骰骰子表达式中
            in_operator = False  # 标记是否在运算符中

            while remaining:
                char = remaining[0]

                # 检查是否是骰骰子表达式的一部分
                if char.lower() == 'd' and not in_dice:
                    # 检查d后面是否是数字
                    if len(remaining) > 1 and remaining[1].isdigit():
                        in_dice = True
                        expr_str += char
                        consumed += char
                        remaining = remaining[1:]
                        continue
                    
                # 检查是否遇到下一个属性名
                if re.match(r'[\u4e00-\u9fa5a-zA-Z]', char) and not in_dice:
                    # 如果是d/D且后面是数字，则继续
                    if char.lower() == 'd' and len(remaining) > 1 and remaining[1].isdigit():
                        expr_str += char
                        consumed += char
                        remaining = remaining[1:]
                        in_dice = True
                        continue
                    else:
                        # 是新的属性名，结束当前表达式
                        break
                    
                # 处理运算符
                if char in ('+', '-', '*', '/', 'd', 'D'):
                    # 如果是运算符，标记状态
                    in_operator = True
                    in_dice = False
                elif char.isdigit() and in_operator:
                    # 运算符后的数字
                    in_operator = False

                # 添加字符到表达式
                expr_str += char
                consumed += char
                remaining = remaining[1:]

            expr_str = expr_str.strip()
            if not expr_str:
                # 表达式为空
                invalid_parts.append(f"{attr}{op}" if op else attr)
                continue
            
            # 获取基础属性值
            if attr not in base_overrides:
                base_value = cls.get_pc_attribute(user_id, platform, attr, group_id)
                base_overrides[attr] = base_value
            else:
                base_value = base_overrides[attr]

            # 计算表达式值
            expr_value, err, expr_desc = cls.calc_expression_with_desc(expr_str, user_id, platform, Proc, overrides)
            if err:
                # 计算出错
                invalid_parts.append(f"{attr}{op or ''}{expr_str}")
                continue
            
            # 应用运算符
            if not op or op == '=':  # 默认或等于操作符是覆盖
                new_value = expr_value
                expr_desc = f"{attr}({base_value})={new_value}"
            elif op == '+':  # 加法
                new_value = base_value + expr_value
                expr_desc = f"{attr}({base_value})+[{expr_desc}]={new_value}"
            elif op == '-':  # 减法
                new_value = base_value - expr_value
                expr_desc = f"{attr}({base_value})-[{expr_desc}]={new_value}"
            elif op == '*':  # 乘法
                new_value = base_value * expr_value
                expr_desc = f"{attr}({base_value})*[{expr_desc}]={new_value}"
            elif op == '/':  # 除法
                if expr_value == 0:
                    new_value = base_value  # 避免除零错误
                    expr_desc = f"{attr}({base_value})/[{expr_desc}(除零错误)]={new_value}"
                else:
                    new_value = base_value // expr_value
                    expr_desc = f"{attr}({base_value})/[{expr_desc}]={new_value}"

            overrides[attr] = new_value
            override_details.append({
                'attr': attr,
                'op': op or '=',
                'expr_str': expr_str,
                'base_value': base_value,
                'new_value': new_value,
                'expr_desc': expr_desc  # 完整的计算过程描述
            })

        return overrides, override_details, invalid_parts, consumed

    @classmethod
    def calc_expression_with_desc(cls, expr_str, user_id, platform, Proc, overrides=None, temp_vars=None, group_id=None):
        """计算表达式字符串的值并返回详细过程"""
        if overrides is None:
            overrides = {}
        if temp_vars is None:
            temp_vars = {}

        # 先处理表达式中的属性引用，优先级: 临时变量 > 覆盖值 > 人物卡属性
        def replace_attr(match):
            attr_name = match.group(1)
            # 1. 查找临时变量
            if attr_name in temp_vars:
                return str(temp_vars[attr_name])
            # 2. 查找覆盖值
            if attr_name in overrides:
                return str(overrides[attr_name])
            # 3. 从人物卡获取
            return str(cls.get_pc_attribute(user_id, platform, attr_name, group_id))

        # 替换所有属性引用为数值
        expr_str = re.sub(r'{(\w+)}', replace_attr, expr_str)
        desc_expr = expr_str  # 用于构建描述

        # 处理骰子表达式
        dice_values = []
        dice_descriptions = []

        # 查找所有骰子表达式
        dice_exprs = re.findall(r'(\d*[dD]\d+|\d+[dD]\d*)', expr_str)
        for dice_expr in dice_exprs:
            rd = OlivaDiceCore.onedice.RD(dice_expr)
            rd.roll()
            if rd.resError is None:
                dice_detail = OlivaDiceCore.onediceOverride.RDDataFormat(
                    data=rd.resDetailData,
                    mode='default'
                )
                dice_total = rd.resInt
                dice_values.append(dice_total)
                dice_descriptions.append(f"{dice_expr}({dice_detail})={dice_total}")
                # 在描述表达式中替换骰子部分
                desc_expr = desc_expr.replace(dice_expr, f"{dice_expr}({dice_detail})={dice_total}", 1)
            else:
                dice_values.append(0)
                dice_descriptions.append(f"{dice_expr}(错误)=0")
                desc_expr = desc_expr.replace(dice_expr, f"{dice_expr}(错误)=0", 1)

        # 替换骰子表达式为计算结果
        def replace_dice(match):
            return str(dice_values.pop(0)) if dice_values else "0"

        calc_expr = re.sub(r'\d*[dD]\d+|\d+[dD]\d*', replace_dice, expr_str)

        # 替换除法为整数除法
        calc_expr = calc_expr.replace('/', '//')

        try:
            result = eval(calc_expr)
            # 构建完整描述
            full_desc = f"{desc_expr}={result}"
            return result, None, full_desc
        except Exception as e:
            Proc.log(4, f"[LexNinjutsu] 计算表达式错误：{str(e)}")
            return 0, "错误", f"{expr_str}(计算错误)"

    @classmethod
    def parse_temporary_assignments(cls, line, temp_vars, user_id, platform, Proc, overrides, group_id):
        """
        处理临时变量赋值：$变量名=<表达式>$
        返回处理后的行和更新后的临时变量字典
        """
        # 使用正则表达式匹配所有$var=<expr>$格式的赋值
        pattern = r'\$([^`=]+)=(<[^>]+>)\$'
        matches = re.finditer(pattern, line)

        new_line = line
        for match in matches:
            full_match = match.group(0)
            var_name = match.group(1).strip()
            expr = match.group(2).strip()

            # 计算表达式值
            expr_desc, total = cls.parse_expression(
                expr, 
                user_id, 
                platform, 
                Proc, 
                overrides=overrides,
                temp_vars=temp_vars,
                group_id=group_id,
                # 试试如果不要这个会有什么奇妙的化学反应，没准会递归下去（
                # is_temp=True
            )

            # 存储临时变量
            temp_vars[var_name] = total

            # 替换为带计算过程的显示格式（与parse_expression一致）
            new_line = new_line.replace(full_match, f"//临时变量：[{var_name}]={expr_desc}//")

        return new_line, temp_vars

    @classmethod
    def parse_expression(cls, expr, user_id, platform, Proc, overrides=None, temp_vars=None, group_id=None, is_temp=False):
        if overrides is None:
            overrides = {}
        if temp_vars is None:
            temp_vars = {}
        
        if not is_temp:
            # 先处理临时变量赋值
            expr, temp_vars = cls.parse_temporary_assignments(
                expr, 
                temp_vars, 
                user_id, 
                platform, 
                Proc, 
                overrides, 
                group_id
            )
    
        # 属性替换函数（优先级：临时变量 > 覆盖值 > 人物卡属性）
        def replace_attr(match, for_display=False):
            attr_name = match.group(1)
            # 1. 查找临时变量
            if attr_name in temp_vars:
                return f"{attr_name}({temp_vars[attr_name]})" if for_display else str(temp_vars[attr_name])
            # 2. 查找覆盖值
            if attr_name in overrides:
                return f"{attr_name}({overrides[attr_name]})" if for_display else str(overrides[attr_name])
            # 3. 从人物卡获取
            value = cls.get_pc_attribute(user_id, platform, attr_name, group_id)
            return f"{attr_name}({value})" if for_display else str(value)
    
        # 描述用表达式（保留属性名）
        desc_expr = re.sub(r'{(\w+)}', lambda m: replace_attr(m, for_display=True), expr)
    
        # 查找所有<骰子表达式>并处理
        dice_blocks = re.findall(r'<([^>]+)>', expr)
        dice_values = []
        dice_descriptions = []
    
        for block in dice_blocks:
            # 处理块内的骰骰子表达式
            block_content = block
            # 生成描述表达式，替换属性为"attr(value)"
            desc_block = re.sub(r'{(\w+)}', lambda m: replace_attr(m, for_display=True), block_content)
            # 生成计算表达式，替换属性为数值
            calc_block = re.sub(r'{(\w+)}', lambda m: replace_attr(m), block_content)
    
            # 处理骰骰子表达式
            block_dice_matches = re.findall(r'(\d*[dD]\d+)', calc_block)
            block_dice_values = []
            block_dice_descriptions = []
    
            for dice_expr in block_dice_matches:
                rd = OlivaDiceCore.onedice.RD(dice_expr)
                rd.roll()
                if rd.resError is None:
                    dice_detail = OlivaDiceCore.onediceOverride.RDDataFormat(
                        data=rd.resDetailData,
                        mode='default'
                    )
                    dice_total = rd.resInt
                    block_dice_values.append(dice_total)
                    block_dice_descriptions.append(f"{dice_expr}({dice_detail})")
                else:
                    block_dice_values.append(0)
                    block_dice_descriptions.append(f"{dice_expr}(错误)")
    
            # 计算块内表达式
            def replace_block_dice(match):
                return str(block_dice_values.pop(0)) if block_dice_values else "0"
    
            # 替换骰骰子表达式为数值
            calc_block = re.sub(r'(\d*[dD]\d+)', replace_block_dice, calc_block)
            # 替换除法为整数除法
            calc_block = calc_block.replace('/', '//')
    
            try:
                block_total = eval(calc_block)
            except Exception as e:
                Proc.log(4, f"[LexNinjutsu] 计算错误：{str(e)}")
                block_total = 0
    
            # 构建块描述（使用desc_block处理后的表达式）
            def replace_block_desc(match):
                return block_dice_descriptions.pop(0) if block_dice_descriptions else "0"
    
            block_desc = re.sub(r'(\d*[dD]\d+)', replace_block_desc, desc_block)
            block_desc = f"[{block_desc}]={block_total}"
    
            dice_values.append(block_total)
            dice_descriptions.append(block_desc)
    
        # 构建最终描述（替换所有<表达式>块）
        def replace_dice_block(match):
            return dice_descriptions.pop(0) if dice_descriptions else "<错误>"
    
        final_desc = re.sub(r'<([^>]+)>', replace_dice_block, desc_expr)
    
        # 计算总和
        total = sum(dice_values) if dice_values else 0
        
        # 后处理
        final_desc = re.sub(r'\((\d+)\(0\)\)', r'({\1})', final_desc)
    
        return final_desc, total

    @classmethod
    def format_name(cls, plugin_event):
        # 获取人物卡名称
        pc_hash = OlivaDiceCore.pcCard.getPcHash(
            plugin_event.data.user_id,
            plugin_event.platform['platform']
        )
        name = OlivaDiceCore.pcCard.pcCardDataGetSelectionKey(pc_hash, str(plugin_event.data.group_id))
        return name or plugin_event.data.sender.get('name', '未知')
    # endregion

    # region 回复
    @classmethod
    def group_message(cls, plugin_event, Proc):
        msg = plugin_event.data.message
        bot_id = plugin_event.bot_info.id
        prefix = f'[OP:at,id={bot_id}]'

        if msg.startswith(prefix):
            content = msg[len(prefix):].strip()
            if not content.startswith(('.','。','/')):
                return
            msg_part = content[1:].strip()
        else:
            if not msg.startswith(('.','。','/')):
                return
            msg_part = msg[1:].strip()
        try:
            raw_msg = msg_part
            user_id = plugin_event.data.user_id
            
            # region 释放忍术
            if raw_msg.startswith(cls.COMMAND_CAST):
                # 获取命令后面的内容
                content = raw_msg[len(cls.COMMAND_CAST):].strip()
                
                # 使用 isMatchWordStart 循环查找忍术名称
                found_ninjutsu = None
                match_type = None
                alias_name = None
                search_name = ""
                remaining = content
                
                # 加载忍术和别名数据
                with open(os.path.join(data_path, "ninjutsu.json"), "r", encoding="utf-8") as f:
                    ninjutsu = json.load(f)
            
                # 构建所有忍术名称列表（包括别名）
                all_names = []
                for level in cls.NINJUTSU_LEVELS:
                    all_names.extend(ninjutsu[level].keys())

                # 添加所有别名
                aliases = {}
                alias_path = os.path.join(data_path, "aliases.json")
                if os.path.exists(alias_path):
                    with open(alias_path, "r", encoding="utf-8") as f:
                        aliases = json.load(f)
                        all_names.extend(aliases.keys())
                
                # 按长度降序排序，优先匹配长名称
                all_names.sort(key=len, reverse=True)

                # 1. 尝试精确匹配/精确别名匹配所有忍术名称
                for name in all_names:
                    if isMatchWordStart(remaining, name, ignoreCase=True):
                        search_name = name
                        found_ninjutsu = name
                        alias_name = found_ninjutsu
                        remaining = getMatchWordStartRight(remaining, name, ignoreCase=True).strip()
                        break

                # 2. 尝试忍术名称拼音匹配
                if not found_ninjutsu and PINYIN_SUPPORT:
                    found_ninjutsu, consumed, match_type = cls.match_by_pinyin(remaining, ninjutsu)
                    if found_ninjutsu:
                        search_name = found_ninjutsu
                        remaining = remaining[consumed:].strip()

                # 3. 尝试别名拼音匹配
                if not found_ninjutsu and PINYIN_SUPPORT and aliases:
                    alias_ninjutsu_data = {level: {} for level in cls.NINJUTSU_LEVELS}
                    alias_ninjutsu_data[cls.NINJUTSU_LEVELS[0]] = {alias: "" for alias in aliases.keys()}
                    
                    found_alias, consumed, tmp_match_type = cls.match_by_pinyin(remaining, alias_ninjutsu_data)
                    if found_alias:
                        found_ninjutsu = found_alias  # 记录匹配到的别名
                        search_name = aliases[found_alias]  # 记录原名
                        alias_name = found_ninjutsu
                        match_type = f'别名{tmp_match_type}'
                        remaining = remaining[consumed:].strip()
                    
                if not found_ninjutsu:
                    plugin_event.reply("忍术不存在，或该忍术暂未被收录！\n释放忍术正确格式：.释放忍术 [名称] (属性1值1 属性2值2 ...)")
                    return
                
                original_name = cls.get_original_name(search_name)
                display_name = search_name if not original_name else original_name
                if alias_name:
                    if alias_name != display_name:
                        display_name += f'(别名：{alias_name})'
                if match_type:
                    display_name += f"({match_type})"
                search_name = original_name if original_name is not None else search_name
                
                # 解析属性覆盖
                overrides = {}
                override_details = []
                invalid_parts = []
                
                overrides, override_details, invalid_parts, consumed = cls.parse_attributes(
                    remaining, 
                    user_id, 
                    plugin_event.platform['platform'], 
                    Proc,
                    group_id=str(plugin_event.data.group_id)
                )
                remaining = remaining[len(consumed):].strip() if consumed else remaining
                
                # 找到忍术描述
                expr = ""
                level = ""
                for lvl in cls.NINJUTSU_LEVELS:
                    if search_name in ninjutsu[lvl]:
                        expr = ninjutsu[lvl][search_name]
                        level = lvl
                        break
                    
                # 替换转义的换行符为实际换行符
                expr = expr.replace('\\n', '\n')
                expr_parts = expr.split('\n')
                result_lines = []
                temp_vars = {}
                
                for part in expr_parts:
                    if part.strip():
                        part_desc, total = cls.parse_expression(
                            part.strip(), 
                            user_id, 
                            plugin_event.platform['platform'], 
                            Proc, 
                            overrides=overrides,
                            temp_vars=temp_vars,
                            group_id=str(plugin_event.data.group_id)
                        )
                        result_lines.append(part_desc)
                
                # 构建回复消息
                reply_msg = f"[{cls.format_name(plugin_event)}] 释放了{level}级忍术 [{display_name}]"
                
                # 添加属性覆盖信息
                if override_details:
                    override_info = []
                    for detail in override_details:
                        override_info.append(detail['expr_desc'])
                    
                    reply_msg += "\n（属性更改: " + ", ".join(override_info) + "）"
                
                # 添加无效部分警告
                if invalid_parts:
                    reply_msg += f"\n!!警告：无效属性更改: {' '.join(invalid_parts)}!!\n"
                
                reply_msg += "\n" + "\n".join(result_lines)
                plugin_event.reply(reply_msg)

            # region 添加忍术
            elif any(raw_msg.startswith(cmd) for cmd in cls.COMMAND_ADD):  # 处理所有添加命令别名
                if not cls.check_permission(plugin_event, 'manager'):
                    plugin_event.reply("你的权限不足，无法添加忍术！")
                    return
            
                # 获取实际使用的命令（去掉前缀）
                used_cmd = next((cmd for cmd in cls.COMMAND_ADD if raw_msg.startswith(cmd)), None)
                content = raw_msg[len(used_cmd):].strip()  # 使用实际命令长度截取内容
                
                if '|' not in content:
                    plugin_event.reply("格式错误，正确格式：添加忍术 [名称|等级|表达式]\n请输入 .忍术帮助 表达式格式 查看表达式格式\n请输入 .忍术帮助 完整示例 查看忍术录入的实例")
                    return
                
                parts = content.split('|', 2)
                if len(parts) < 3:
                    plugin_event.reply("格式错误，正确格式：添加忍术 [名称|等级|表达式]\n请输入 .忍术帮助 表达式格式 查看表达式格式\n请输入 .忍术帮助 完整示例 查看忍术录入的实例")
                    return
                
                name, level, expr = parts
                level = level.strip().upper()
                name = name.strip().upper()
                if level not in cls.NINJUTSU_LEVELS:
                    plugin_event.reply(f"请输入正确的忍术等级（E/D/C/B/A/S/禁术）！")
                    return
                
                with open(os.path.join(data_path, "ninjutsu.json"), "r", encoding="utf-8") as f:
                    ninjutsu = json.load(f)
                    # 检查所有等级中是否已存在同名忍术
                    for lvl in cls.NINJUTSU_LEVELS:
                        if name.strip() in ninjutsu[lvl]:
                            plugin_event.reply(f"忍术 [{name}] 已存在，请先删除后再添加")
                            return
                
                if cls.save_ninjutsu(name, level, expr):
                    plugin_event.reply(f"已添加{level}级忍术 [{name}]")
                else:
                    # 检查是否是别名冲突
                    original_name = cls.get_original_name(name)
                    if original_name is not None:
                        plugin_event.reply(f"名称 [{name}] 与现有别名冲突，请使用其他名称")
                    else:
                        plugin_event.reply(f"忍术 [{name}] 已存在，请先删除后再添加或者更改")

            # region 修改忍术
            elif any(raw_msg.startswith(cmd) for cmd in cls.COMMAND_UPDATE):
                if not cls.check_permission(plugin_event, 'manager'):
                    plugin_event.reply("你的权限不足，无法修改忍术！")
                    return

                # 获取实际使用的命令（去掉前缀）
                used_cmd = next((cmd for cmd in cls.COMMAND_UPDATE if raw_msg.startswith(cmd)), None)
                content = raw_msg[len(used_cmd):].strip()

                if '|' not in content:
                    plugin_event.reply("格式错误，正确格式：.修改忍术 [名称|新等级|新表达式]\n可以使用别名，但修改的是原名对应的忍术")
                    return

                parts = content.split('|', 2)
                if len(parts) < 3:
                    plugin_event.reply("格式错误，正确格式：.修改忍术 [名称|新等级|新表达式]\n可以使用别名，但修改的是原名对应的忍术")
                    return

                input_name, new_level, new_expr = parts
                new_level = new_level.strip().upper()
                input_name = input_name.strip().upper()

                # 获取原名（如果是别名）
                original_name = cls.get_original_name(input_name) or input_name

                if new_level not in cls.NINJUTSU_LEVELS:
                    plugin_event.reply(f"请输入正确的忍术等级（E/D/C/B/A/S/禁术）！")
                    return

                with open(os.path.join(data_path, "ninjutsu.json"), "r+", encoding="utf-8") as f:
                    ninjutsu = json.load(f)

                    # 查找忍术是否存在
                    found = False
                    old_level = None
                    for lvl in cls.NINJUTSU_LEVELS:
                        if original_name in ninjutsu[lvl]:
                            old_level = lvl
                            found = True
                            break
                        
                    if not found:
                        plugin_event.reply(f"忍术 [{original_name}] 不存在，请先添加")
                        return

                    # 如果等级没变，直接更新表达式
                    if old_level == new_level:
                        ninjutsu[old_level][original_name] = new_expr.strip()
                    else:
                        # 等级变化，需要移动到新等级
                        old_expr = ninjutsu[old_level].pop(original_name)
                        ninjutsu[new_level][original_name] = new_expr.strip()

                    f.seek(0)
                    json.dump(ninjutsu, f, indent=4, ensure_ascii=False)
                    f.truncate()

                # 构建回复消息
                reply_msg = f"已{'更新' if old_level == new_level else '修改并移动'}忍术 [{original_name}] ({old_level}→{new_level})"
                if input_name != original_name:
                    reply_msg += f"\n(通过别名 [{input_name}] 找到原名)"

                plugin_event.reply(reply_msg)

            # region 删除忍术
            elif raw_msg.startswith(cls.COMMAND_DEL):
                if not cls.check_permission(plugin_event, 'manager'):
                    plugin_event.reply("你的权限不足，无法删除忍术！")
                    return

                name = raw_msg[len(cls.COMMAND_DEL):].strip().upper()
                with open(os.path.join(data_path, "ninjutsu.json"), "r+", encoding="utf-8") as f:
                    ninjutsu = json.load(f)
                    
                    found = False
                    # 在所有等级中查找并删除忍术
                    for lvl in cls.NINJUTSU_LEVELS:
                        if name in ninjutsu[lvl]:
                            del ninjutsu[lvl][name]
                            found = True
                            break
                    
                    if not found:
                        plugin_event.reply(f"忍术 [{name}] 不存在")
                        return
                    
                    f.seek(0)
                    json.dump(ninjutsu, f, indent=4, ensure_ascii=False)
                    f.truncate()
                
                # 检查并删除相关别名
                alias_path = os.path.join(data_path, "aliases.json")
                if os.path.exists(alias_path):
                    with open(alias_path, "r+", encoding="utf-8") as f:
                        aliases = json.load(f)
                        # 找出所有指向该忍术的别名
                        aliases_to_delete = [k for k, v in aliases.items() if v == name]
                        for alias in aliases_to_delete:
                            del aliases[alias]
                        
                        f.seek(0)
                        json.dump(aliases, f, indent=4, ensure_ascii=False)
                        f.truncate()
                
                plugin_event.reply(f"已删除忍术 [{name}]" + (f"及其 {len(aliases_to_delete)} 个别名" if aliases_to_delete else ""))

            # region 管理权限
            elif raw_msg.startswith(cls.COMMAND_MANAGE):
                if not cls.is_dice_master(plugin_event):
                    plugin_event.reply("你的权限不足，无法添加权限！(admin权限的可以给manager权限)")
                    return

                parts = raw_msg[len(cls.COMMAND_MANAGE):].strip().split()
                if len(parts) != 3 or parts[0] not in ['admin', 'manager'] or parts[1] not in ['add', 'del']:
                    plugin_event.reply("格式：管理忍术 [admin/manager] [add/del] [用户ID]")
                    return

                perm_type, action, target = parts
                
                # 检查是否是骰主尝试给自己添加权限
                user_hash = OlivaDiceCore.userConfig.getUserHash(
                    target,
                    'user',
                    plugin_event.platform['platform']
                )
                if action == 'add' and OlivaDiceCore.ordinaryInviteManager.isInMasterList(
                    plugin_event.bot_info.hash,
                    user_hash
                ):
                    plugin_event.reply("不能给骰主添加额外权限")
                    return

                with open(os.path.join(data_path, "permissions.json"), "r+", encoding="utf-8") as f:
                    perms = json.load(f)
                    
                    # 添加权限前检查是否已有其他权限
                    if action == 'add' and cls.check_permission_exists(target):
                        plugin_event.reply("该用户已有其他权限，请先移除原有权限")
                        return
                        
                    target_list = perms.setdefault(perm_type, [])
                    if action == 'add' and target not in target_list:
                        target_list.append(target)
                        # 确保从另一权限列表中移除
                        other_type = 'manager' if perm_type == 'admin' else 'admin'
                        if target in perms.get(other_type, []):
                            perms[other_type].remove(target)
                    elif action == 'del' and target in target_list:
                        target_list.remove(target)
                    
                    f.seek(0)
                    json.dump(perms, f, indent=4, ensure_ascii=False)
                    f.truncate()
                
                plugin_event.reply(f"已{action}用户 {target} 的{perm_type}权限")

            # region 增加别名
            elif any(raw_msg.startswith(cmd) for cmd in cls.COMMAND_ADD_ALIAS):
                if not cls.check_permission(plugin_event, 'manager'):
                    plugin_event.reply("你的权限不足，无法添加忍术别名！")
                    return
                
                # 获取实际使用的命令（去掉前缀）
                used_cmd = next((cmd for cmd in cls.COMMAND_ADD_ALIAS if raw_msg.startswith(cmd)), None)
                content = raw_msg[len(used_cmd):].strip()
                
                if '|' not in content:
                    plugin_event.reply("格式错误，正确格式：添加忍术别名 [别名|原名]")
                    return
                
                parts = content.split('|', 1)
                if len(parts) < 2:
                    plugin_event.reply("格式错误，正确格式：添加忍术别名 [别名|原名]")
                    return
                
                alias_name, original_name = parts
                original_name = original_name.strip().upper()
                alias_name = alias_name.strip().upper()
                
                success, message = cls.add_alias(original_name, alias_name)
                plugin_event.reply(message)

            # region 删除别名
            elif any(raw_msg.startswith(cmd) for cmd in cls.COMMAND_DEL_ALIAS):
                if not cls.check_permission(plugin_event, 'manager'):
                    plugin_event.reply("你的权限不足，无法删除忍术别名！")
                    return
                
                # 获取实际使用的命令（去掉前缀）
                used_cmd = next((cmd for cmd in cls.COMMAND_DEL_ALIAS if raw_msg.startswith(cmd)), None)
                alias_name = raw_msg[len(used_cmd):].strip().upper()
                
                success, message = cls.remove_alias(alias_name)
                plugin_event.reply(message)

            # region 查询别名
            elif any(raw_msg.startswith(cmd) for cmd in cls.COMMAND_QUERY_ALIAS):
                # 获取忍术名称
                name = raw_msg.split(maxsplit=1)
                if len(name) < 2:
                    plugin_event.reply("格式错误，正确格式：.查询别名 [忍术名称]")
                    return

                query_name = name[1].strip().upper()

                # 尝试获取原名（如果输入的是别名）
                original_name = cls.get_original_name(query_name)
                if original_name:
                    display_name = original_name
                else:
                    display_name = query_name

                # 加载别名数据
                alias_path = os.path.join(data_path, "aliases.json")
                if not os.path.exists(alias_path):
                    plugin_event.reply(f"忍术 [{display_name}] 没有别名")
                    return

                with open(alias_path, "r", encoding="utf-8") as f:
                    aliases = json.load(f)

                # 获取所有别名
                alias_list = []
                for alias, orig in aliases.items():
                    if orig == display_name:
                        alias_list.append(alias)

                if not alias_list:
                    plugin_event.reply(f"忍术 [{display_name}] 没有别名")
                else:
                    plugin_event.reply(f"忍术 [{display_name}] 的别名有：\n" + ", ".join([f"`{alias_name}`" for alias_name in alias_list]))

            # region 查询忍术列表
            elif any(raw_msg.startswith(cmd) for cmd in cls.COMMAND_LIST):  # 处理所有列表命令别名
                # 检查是否有指定等级
                parts = raw_msg.split()
                level_filter = None
                if len(parts) > 1:
                    level_filter = parts[1].strip().upper()
                    if level_filter not in cls.NINJUTSU_LEVELS:
                        level_filter = None

                # 如果没有指定等级，提示需要输入等级
                if not level_filter:
                    plugin_event.reply("请指定要查看的忍术等级(E/D/C/B/A/S/禁术)，例如：.查看忍术 E")
                    return

                with open(os.path.join(data_path, "ninjutsu.json"), "r", encoding="utf-8") as f:
                    ninjutsu = json.load(f)

                # 构建忍术列表
                nin_list = []
                for level in cls.NINJUTSU_LEVELS:
                    if level_filter and level != level_filter:
                        continue
                    if ninjutsu[level]:
                        level_nin = [", ".join([f"`{name}`" for name in ninjutsu[level].keys()])]
                        nin_list.extend(level_nin)

                if not nin_list:
                    plugin_event.reply(f"没有找到{level_filter}级的忍术")
                    return

                reply_msg = f"{level_filter}级忍术列表：\n" + "\n".join(nin_list)
                plugin_event.reply(reply_msg)

            # region 随机忍术
            elif any(raw_msg.startswith(cmd) for cmd in cls.COMMAND_RANDOM):
                # 获取命令后面的内容
                content = raw_msg.split(maxsplit=1)
                level_filter = None
                if len(content) > 1:
                    level_filter = content[1].strip().upper()
                    if level_filter not in cls.NINJUTSU_LEVELS:
                        plugin_event.reply(f"请输入正确的忍术等级（E/D/C/B/A/S/禁术）或留空完全随机！")
                        return

                with open(os.path.join(data_path, "ninjutsu.json"), "r", encoding="utf-8") as f:
                    ninjutsu = json.load(f)

                # 构建候选忍术列表
                candidates = []
                for level in cls.NINJUTSU_LEVELS:
                    if level_filter and level != level_filter:
                        continue
                    candidates.extend([(name, level) for name in ninjutsu[level].keys()])

                if not candidates:
                    plugin_event.reply(f"没有找到{'指定等级' if level_filter else ''}的忍术")
                    return

                # 随机选择一个忍术
                selected_name, selected_level = random.choice(candidates)

                # 构建释放命令
                release_cmd = f"{cls.COMMAND_CAST} {selected_name}"

                # 模拟释放忍术
                plugin_event.data.message = f".{release_cmd}"
                cls.group_message(plugin_event, Proc)

            # region 帮助命令
            elif any(raw_msg.startswith(cmd) for cmd in cls.COMMAND_HELP):  # 处理所有帮助命令别名
                help_arg = raw_msg.split(maxsplit=1)
                if len(help_arg) == 1:  # 只有基础命令
                    help_msg = """输入以下命令查看详细帮助：
.忍术帮助 命令列表 - 查看所有可用命令
.忍术帮助 表达式格式 - 查看表达式编写说明
.忍术帮助 权限说明 - 查看权限等级说明
.忍术帮助 别名管理 - 查看别名管理说明
.忍术帮助 完整示例 - 查看完整的忍术添加示例"""
                else:
                    arg = help_arg[1].strip()
                    if arg == "命令列表":
                        help_msg = """命令列表：
.释放忍术 [名称] (属性1值1 属性2值2 ...) - 释放指定的忍术(空格可加可不加，属性可省略，默认从人物卡获取)
.查看忍术 [等级] - 查看所有可用的忍术(可指定等级：E/D/C/B/A/S/禁术)
.添加忍术 [名称|等级|表达式] - 添加新忍术(等级：E/D/C/B/A/S/禁术)
.修改忍术 [名称|新等级|新表达式] - 修改已有忍术(可以使用别名)
.删除忍术 [名称] - 删除忍术
.添加别名 [别名|原名] - 为忍术添加别名
.删除别名 [别名] - 删除忍术别名
.查询别名 [别名或原名] - 查询忍术的所有别名
.随机忍术 (等级) - 随机释放(指定等级的)忍术
.管理忍术 [admin/manager] [add/del] [QQ号] - 管理权限"""
                    elif arg == "表达式格式":
                        help_msg = """表达式格式说明：
1. 用<>包裹住数据计算部分(支持加减乘除和骰子计算式)
2. 用{}包裹从人物卡里面读取的数值(如{忍术技艺})
3. 用$$包裹临时变量(临时变量在后面用花括号{}包裹调用，例如{临时变量})
4. 换行符使用\\n表示
5. 支持标准数学运算符：+ - * / // %"""
                    elif arg == "权限说明":
                        help_msg = """权限说明：
- 正常用户：可以释放忍术和查看忍术
- manager/群管/群主: 可以添加/删除忍术及正常用户所有权限
- admin: 可以管理manager权限及拥有manager的权限
- 骰主: 可以管理所有权限及使用全部功能"""
                    elif arg == "别名管理":
                        help_msg = """别名管理说明：
1. 别名不能与原名相同
2. 一个原名可以对应多个别名
3. 一个别名只能对应一个原名
4. 别名不能与已有忍术名称冲突
5. 添加/删除别名需要manager及以上权限

命令格式：
.添加忍术别名 [别名|原名]
.删除忍术别名 [别名]
.查询别名 [别名或原名]"""
                    elif arg == "完整示例" or arg == "忍术模板":
                        help_msg = """完整示例：
.添加忍术 纳米悠悠球|D|类型/派系/属性：攻击/科学/纳米\\n蕾克拉消耗：35\\n出手速度：6\\n忍术速度：<2D4+{身手}>\\n$tRoll=<2d4>$\\n强度：<{tRoll}+{忍术技艺}>\\n或 <{tRoll}+{蛮力}>\\n伤害：<3D4+{忍术技艺}>\\n力量对拼：否\\n特效：蕾克拉球体可以存在一段时间本回合内闪避与格挡检定+<1D4>。\\n说明：将蕾克拉聚集为球体，在周身环绕，击退敌人，可攻可守，十分灵活！"""
                    else:
                        help_msg = "未知的帮助命令，可用命令：命令列表、表达式格式、权限说明、完整示例"

                    if not PINYIN_SUPPORT:
                        help_msg += "\n\n注意：拼音匹配功能未启用，请使用命令 `pip install pypinyin` 安装pypinyin库"
    
                plugin_event.reply(help_msg)

        except Exception as e:
            Proc.log(4, f"[LexNinjutsu] 错误：{str(e)}")
            plugin_event.reply("处理命令时发生错误")

# region 特殊函数
def isMatchWordStart(data, key, ignoreCase=True, fullMatch=False, isCommand=False):
    tmp_output = False
    flag_skip = False
    tmp_data = data
    tmp_keys = [key] if isinstance(key, str) else key
    if isCommand:
        if 'replyContextFliter' in OlivaDiceCore.crossHook.dictHookList:
            for k in tmp_keys:
                if k in OlivaDiceCore.crossHook.dictHookList['replyContextFliter']:
                    tmp_output = False
                    flag_skip = True
                    break
    if not flag_skip:
        if ignoreCase:
            tmp_data = tmp_data.lower()
            tmp_keys = [k.lower() for k in tmp_keys]
        for tmp_key in tmp_keys:
            if not fullMatch and len(tmp_data) >= len(tmp_key):
                if tmp_data[:len(tmp_key)] == tmp_key:
                    tmp_output = True
                    break
            elif fullMatch and tmp_data == tmp_key:
                tmp_output = True
                break
    return tmp_output

def getMatchWordStartRight(data, key, ignoreCase=True):
    tmp_output_str = ''
    tmp_data = data
    tmp_keys = [key] if isinstance(key, str) else key
    if ignoreCase:
        tmp_data = tmp_data.lower()
        tmp_keys = [k.lower() for k in tmp_keys]
    for tmp_key in tmp_keys:
        if len(tmp_data) > len(tmp_key):
            if tmp_data[:len(tmp_key)] == tmp_key:
                tmp_output_str = data[len(tmp_key):]
                break
    return tmp_output_str