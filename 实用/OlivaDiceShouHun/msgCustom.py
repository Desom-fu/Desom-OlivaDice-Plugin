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
    'strShResult': '[{tName}]进行狩魂者检定:\n出值: {tFrontResult}\n挑战值: {tBackResult} {tSkillCheckReasult} {tSuccessLevel}',
    'strShHideShow': '[{tName}]进行了暗狩魂者检定',
    'strShHide': '于群[{tGroupId}]中[{tName}]进行狩魂者暗检定:\n出值: {tFrontResult}\n挑战值: {tBackResult} {tSkillCheckReasult} {tSuccessLevel}',
    'strShResultAtOther': '[{tUserName}]帮[{tName}]进行狩魂者检定:\n出值: {tFrontResult}\n挑战值: {tBackResult} {tSkillCheckReasult} {tSuccessLevel}',
    'strShHideShowAtOther': '[{tUserName}]帮[{tName}]进行了狩魂者暗检定',
    'strShHideAtOther': '于群[{tGroupId}]中[{tUserName}]帮[{tName}]进行暗狩魂者检定:\n出值: {tFrontResult}\n挑战值: {tBackResult} {tSkillCheckReasult} {tSuccessLevel}',
    'strShSuccessLevel': '成功等级: {tSuccessLevelInt}',
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
    'strShError': '【.sh】指令\n检定错误'
}

dictHelpDocTemp = {
    'sh': '''【狩魂者检定】
.sh(h)(b/p数字)(x数字+)(掷骰表达式)(#)(b/p数字)(x数字+)(掷骰表达式)

掷骰表达式中可以包含技能名，技能名会自动替换成对应的属性值
h 代表暗骰，b/p数字 代表加/减多少成功等级，默认为1
用 # 来分隔前式和后式
# 后的 b/p数字 代表对方的奖励/惩罚成功等级
出式已经默认带有 1D20，无需后续添加（若进行添加且后续为加算则会被忽略）
如果带有 x，则为指定 1D20 的值，之后必须跟着 '+'
特殊的，如果出式中的 x 后面跟的数字为 0，则代表本次检定不带 1D20
挑战式中的 x 不能为 0，最小为 1 
如果没有 # 分割，则默认挑战式为 10
若出值为指定数字，则出值不带 1D20
成功等级计算为 (前式-后式)/5 向上取整
出值里的 D20 会自动计算大成功/大失败带来的额外成功等级，挑战值中每个 D20 里面的大成功和大失败也会影响成功等级（固定值也会影响）

示例：如要进行一次有三个加骰和两个时髦骰的掷骰，则输入.sh3d4+2d6
示例2：如要进行一次D20的值被固定为15，有四个加骰和三个时髦骰，连续第二次进行反击的掷骰，去对抗敌人有两个加骰的攻击掷骰，则输入.shp2x15+4d4+3d6#d20+2d4

可由管理员及以上权限的人进行代骰
代骰方式：在指令的末尾@目标用户''',

    'shst':'''【狩魂者跑团数据录入帮助文档】
1、将骰子拉入群聊后，请先使用[.set temp shouhun]，让本群套用狩魂者模板（只需输入一次，其他人无需再输入）
2、玩家在填写完角色卡并审核通过后，将附表“信息总览表与检定公式”中的.st数据复制粘贴，输入群内，这样就完成了基础数据的录入。
3、玩家输入[.sn]或者[.sn template]，改变名片格式。
4、玩家输入[.sn auto on]，让名片数据能够自动变化。'''
}
