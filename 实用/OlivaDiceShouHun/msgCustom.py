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
import OlivaDiceCore
import OlivaDiceShouHun

dictStrCustomDict = {}

dictStrCustom = {
    'strShResult': '[{tName}]进行狩魂者检定:\n出值: {tFrontResult}\n挑战值: {tBackResult} {tSkillCheckReasult} {tSuccessLevel}{tShmAdd}',
    'strShHideShow': '[{tName}]进行了暗狩魂者检定',
    'strShHide': '于群[{tGroupId}]中[{tName}]进行狩魂者暗检定:\n出值: {tFrontResult}\n挑战值: {tBackResult} {tSkillCheckReasult} {tSuccessLevel}{tShmAdd}',
    'strShResultAtOther': '[{tUserName}]帮[{tName}]进行狩魂者检定:\n出值: {tFrontResult}\n挑战值: {tBackResult} {tSkillCheckReasult} {tSuccessLevel}{tShmAdd}',
    'strShHideShowAtOther': '[{tUserName}]帮[{tName}]进行了狩魂者暗检定',
    'strShHideAtOther': '于群[{tGroupId}]中[{tUserName}]帮[{tName}]进行暗狩魂者检定:\n出值: {tFrontResult}\n挑战值: {tBackResult} {tSkillCheckReasult} {tSuccessLevel}{tShmAdd}',
    'strShSuccessLevel': '成功等级: {tSuccessLevelInt}',
    'strShShmAdd': '\nshm: {tShmOld}+{tShmAddValue}={tShmNew}',
    'strShError': '狩魂者检定错误: {tResult}\n查询正确检定指令请使用.help sh查看\n录卡规则请使用.help shst查看'
}

dictStrConst = {
}

dictGValue = {
}

dictTValue = {
}

dictStrCustomNote = {
    'strShResult': '【.sh】指令\n进行狩魂者检定',
    'strShHideShow': '【.sh】指令\n进行暗狩魂者检定回复词（群内）',
    'strShHide': '【.sh】指令\n进行暗狩魂者检定回复词（结果）',
    'strShResultAtOther': '【.sh】代骰指令\n代他人进行狩魂者检定',
    'strShHideShowAtOther': '【.sh】代骰指令\n代他人进行暗狩魂者检定回复词（群内）',
    'strShHideAtOther': '【.sh】代骰指令\n代他人进行暗狩魂者检定回复词（结果）',
    'strShSuccessLevel': '【.sh】指令\n成功等级',
    'strShShmAdd': '【.sh】指令\nshm增加显示',
    'strShError': '【.sh】指令\n检定错误'
}

dictHelpDocTemp = {
    '狩魂者': '''【狩魂者模块 - 总帮助】

本模块提供《鬼喊抓鬼》狩魂者跑团规则的检定系统。

检定指令：
• .sh - 狩魂者检定

详细帮助：
• .help sh - 查看狩魂者检定详细说明
• .help shst - 查看人物卡录入帮助''',

    'sh': '''【狩魂者检定】
.sh(h)(m)(b/p数字)(x数字+)(掷骰表达式)(~掷骰表达式)(#)(b/p数字)(x数字+)(掷骰表达式)

参数说明：
- h：暗骰
- m：去除默认的1D20（仅前式可用）
- b/p数字：加/减成功等级（默认为1）
- x数字+：指定1D20的值（x参数会覆盖m参数）
- ~表达式：~后的计算结果加到前式结果中，同时自动加到人物卡的shm属性（仅前式可用）
- #：分隔前式和后式
- 技能名：会自动替换成对应的属性值

检定规则：
- 出式默认带有1D20（可用m参数去除）
- 若出值为纯数字，则不带1D20
- 如果没有#分割，默认挑战值为10
- 成功等级 = (前式-后式)/5 向上取整
- D20大成功/大失败会影响成功等级
- 挑战值中的D20和固定值也会影响成功等级

参数组合：
- .sh3d4+2d4           // 1D20+3d4+2d4
- .shp2x15+4d4+3d6#d20+2d4  // 固定D20=15，惩罚2级
- .shh9d4~3d6#15       // 1D20+9d4+3d6，3d6加到shm，暗骰
- .shm5d6              // 5d6（无D20）

代骰说明：
可由管理员及以上权限的人进行代骰
代骰方式：在指令的末尾@目标用户''',

    'shst':'''【狩魂者跑团数据录入帮助文档】
1、将骰子拉入群聊后，请先使用[.set temp shouhun]，让本群套用狩魂者模板（只需输入一次，其他人无需再输入）
2、玩家在填写完角色卡并审核通过后，将附表“信息总览表与检定公式”中的.st数据复制粘贴，输入群内，这样就完成了基础数据的录入。
3、玩家输入[.sn]或者[.sn template]，改变名片格式。
4、玩家输入[.sn auto on]，让名片数据能够自动变化。''',

    'shouhun': '&sh',
    '狩魂': '&狩魂者',
    '鬼喊': '&狩魂者',
    '鬼喊抓鬼': '&狩魂者',
}
