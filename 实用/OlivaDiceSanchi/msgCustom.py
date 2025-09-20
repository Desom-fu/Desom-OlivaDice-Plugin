# -*- encoding: utf-8 -*-
'''
_______________________    _________________________________________
__  __ \__  /____  _/_ |  / /__    |__  __ \___  _/_  ____/__  ____/
_  / / /_  /  __  / __ | / /__  /| |_  / / /__  / _  /    __  __/   
/ /_/ /_  /____/ /  __ |/ / _  ___ |  /_/ /__/ /  / /___  _  /___   
\____/ /_____/___/  _____/  /_/  |_/_____/ /___/  \____/  /_____/   

@File      :   msgCustom.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaDiceCore
import OlivaDiceSanchi

dictStrCustomDict = {}

dictStrCustom = {
    # .tq 铜钱卦占卜相关消息
    'strTQResult': '[{tName}]进行占卜{tExprShow}，掷出{tOriginalNumber}枚铜钱{tExtraCoinsText}，结果为: {tResult}\n阴: {tYinNumber}次；阳: {tYangNumber}次{tTransformText}',
    'strTQResultMore': '[{tName}]进行占卜{tExprShow}，掷了{tTime}次，每次掷出{tOriginalNumber}枚铜钱{tAllExtraCoinsText}，结果为: \n{tResult}\n总和次数：阴: {tYinNumber}次；阳: {tYangNumber}次{tBPText}',
    'strTQError': '三尺之下占卜错误: {tResult}\n请使用[.help r]查看掷骰帮助，或使用[.help onedice]查看先进的OneDice标准。\n请通过.help sanchi查看正确占卜格式',
    'strTQHide': '[{tName}]在群({tGroupId})中进行暗中占卜{tExprShow}：\n掷出{tOriginalNumber}枚铜钱{tExtraCoinsText}，结果为: {tResult}\n阴: {tYinNumber}次；阳: {tYangNumber}次{tTransformText}',
    'strTQHideShow': '[{tName}]进行暗中占卜',
    'strTQHideMore': '[{tName}]在群({tGroupId})中进行暗中占卜{tExprShow}：\n掷了{tTime}次，每次掷出{tOriginalNumber}枚铜钱{tAllExtraCoinsText}，结果为: \n{tResult}\n总和次数：阴: {tYinNumber}次；阳: {tYangNumber}次{tBPText}',
    'strTQHideShowMore': '[{tName}]进行暗中占卜',
    'strTQAtOther': '为[{tName}]进行占卜{tExprShow}，掷出{tOriginalNumber}枚铜钱{tExtraCoinsText}，结果为: {tResult}\n阴: {tYinNumber}次；阳: {tYangNumber}次{tTransformText}',
    'strTQAtOtherMore': '为[{tName}]进行占卜{tExprShow}，掷了{tTime}次，每次掷出{tOriginalNumber}枚铜钱{tAllExtraCoinsText}，结果为: \n{tResult}\n总和次数：阴: {tYinNumber}次；阳: {tYangNumber}次{tBPText}',
    'strTQHideAtOther': '[{tName}]在群({tGroupId})中的暗中占卜结果{tExprShow}：\n掷出{tOriginalNumber}枚铜钱{tExtraCoinsText}，结果为: {tResult}\n阴: {tYinNumber}次；阳: {tYangNumber}次{tTransformText}',
    'strTQHideShowAtOther': '为[{tName}]进行暗中占卜',
    'strTQHideAtOtherMore': '[{tName}]在群({tGroupId})中的暗中占卜结果{tExprShow}：\n掷了{tTime}次，每次掷出{tOriginalNumber}枚铜钱{tAllExtraCoinsText}，结果为: \n{tResult}\n总和次数：阴: {tYinNumber}次；阳: {tYangNumber}次{tBPText}',
    'strTQHideShowAtOtherMore': '为[{tName}]进行暗中占卜',
    
    # .tqa 三尺之下检定相关消息
    'strTQAResult': '[{tName}]进行三尺之下检定\n属性：{tAttrResult} 难度：{tDifficultyResult}\n{tLevelDesc}{tExtraDifficultyText}\n铜钱：{tCoinsResult}{tTransformText}\n阳爻：{tYangCount}个（需要{tRequiredYang}个）→{tSuccessText}',
    'strTQAHideShow': '[{tName}]进行了暗三尺之下检定',
    'strTQAHide': '于群[{tGroupId}]中[{tName}]进行三尺之下暗检定:\n属性：{tAttrResult} 难度：{tDifficultyResult}\n{tLevelDesc}{tExtraDifficultyText}\n铜钱：{tCoinsResult}{tTransformText}\n阳爻：{tYangCount}个（需要{tRequiredYang}个）→{tSuccessText}',
    'strTQAAtOther': '[{tUserName}]帮[{tName}]进行三尺之下检定:\n属性：{tAttrResult} 难度：{tDifficultyResult}\n{tLevelDesc}{tExtraDifficultyText}\n铜钱：{tCoinsResult}{tTransformText}\n阳爻：{tYangCount}个（需要{tRequiredYang}个）→{tSuccessText}',
    'strTQAHideShowAtOther': '[{tUserName}]帮[{tName}]进行了暗三尺之下检定',
    'strTQAHideAtOther': '于群[{tGroupId}]中[{tUserName}]帮[{tName}]进行三尺之下暗检定:\n属性：{tAttrResult} 难度：{tDifficultyResult}\n{tLevelDesc}{tExtraDifficultyText}\n铜钱：{tCoinsResult}{tTransformText}\n阳爻：{tYangCount}个（需要{tRequiredYang}个）→{tSuccessText}',
    'strTQAError': '三尺之下检定错误: {tResult}\n请使用[.help r]查看掷骰帮助，或使用[.help onedice]查看先进的OneDice标准。\n请通过.help sanchi查看正确检定格式',
    'strTQAFormatError': 'tqa命令格式错误，需要用#分隔属性和难度\n正确格式: .tqa 属性#难度',
    
    # .tqav 三尺之下对抗相关消息  
    'strTQAVResult': '\n{tName}：{tMyAttrResult}{tMyTransformText}\n铜钱：{tMyCoinsResult} → 阳爻{tMyYangCount}个\n总计：{tMyYangCount}+{tMyAttrValue}={tMyTotal}\n\n{tName01}：{tOtherAttrResult}{tOtherTransformText}\n铜钱：{tOtherCoinsResult} → 阳爻{tOtherYangCount}个\n总计：{tOtherYangCount}+{tOtherAttrValue}={tOtherTotal}\n\n结果：{tContestResult}',
    'strTQAVError': '三尺之下对抗错误: {tResult}\n请使用[.help r]查看掷骰帮助，或使用[.help onedice]查看先进的OneDice标准。\n请通过.help sanchi查看正确对抗格式',
    'strTQAVNoAtError': 'tqav命令必须@对方才能使用\n正确格式: .tqav 自己属性#对方属性 @对方',
    'strTQAVFormatError': 'tqav命令格式错误，需要用#分隔自己和对方的参数\n正确格式: .tqav 自己属性#对方属性 @对方',
    
    # 通用错误消息
    'strCoinRollError': '铜钱投掷出错',
    'strMyExprError': '自己的表达式解析错误: {tResult}',
    'strOtherExprError': '对方的表达式解析错误: {tResult}',
    'strAttrExprError': '属性表达式解析错误: {tResult}',
    'strDifficultyExprError': '难度表达式解析错误: {tResult}'
}

dictStrConst = {
}

dictGValue = {
}

dictTValue = {
    # 基础用户信息
    'tName': '用户',
    'tUserName': '用户',
    'tName01': '对方',
    'tGroupId': '0',
    
    # .tq 占卜相关
    'tExprShow': '',
    'tOriginalNumber': '3',
    'tNumber': '3',
    'tTime': '1',
    'tResult': '',
    'tYinNumber': '0',
    'tYangNumber': '0',
    'tTransformText': '',
    'tExtraCoinsText': '',
    'tAllExtraCoinsText': '',
    'tBPText': '',
    
    # .tqa 检定相关
    'tAttrResult': '0',
    'tDifficultyResult': '0',
    'tCoinsResult': '阴、阴、阴',
    'tYangCount': '0',
    'tRequiredYang': '1',
    'tLevelDesc': '检定',
    'tExtraDifficultyText': '',
    'tSuccessText': '失败',
    
    # .tqav 对抗相关
    'tMyAttrResult': '0',
    'tMyAttrValue': '0',
    'tMyCoinsResult': '阴、阴、阴',
    'tMyYangCount': '0',
    'tMyTotal': '0',
    'tMyTransformText': '',
    'tOtherAttrResult': '0',
    'tOtherAttrValue': '0',
    'tOtherCoinsResult': '阴、阴、阴',
    'tOtherYangCount': '0',
    'tOtherTotal': '0',
    'tOtherTransformText': '',
    'tContestResult': '平手',
    
    # 错误处理
    'tRollPara': '',
    'tResult': ''
}

dictStrCustomNote = {
    # .tq 铜钱卦占卜相关
    'strTQResult': '【.tq】指令\n占卜结果',
    'strTQResultMore': '【.tq】指令\n多次占卜结果',
    'strTQError': '【.tq】指令\n占卜错误',
    'strTQHide': '【.tq】指令\n暗骰占卜结果',
    'strTQHideShow': '【.tq】指令\n暗骰占卜提示',
    'strTQHideMore': '【.tq】指令\n暗骰多次占卜结果',
    'strTQHideShowMore': '【.tq】指令\n暗骰多次占卜提示',
    'strTQAtOther': '【.tq】指令\n代骰占卜结果',
    'strTQAtOtherMore': '【.tq】指令\n代骰多次占卜结果',
    'strTQHideAtOther': '【.tq】指令\n暗骰代骰占卜结果',
    'strTQHideShowAtOther': '【.tq】指令\n暗骰代骰占卜提示',
    'strTQHideAtOtherMore': '【.tq】指令\n暗骰代骰多次占卜结果',
    'strTQHideShowAtOtherMore': '【.tq】指令\n暗骰代骰多次占卜提示',
    
    # .tqa 三尺之下检定相关
    'strTQAResult': '【.tqa】指令\n三尺之下检定结果',
    'strTQAHideShow': '【.tqa】指令\n暗三尺之下检定提示',
    'strTQAHide': '【.tqa】指令\n暗三尺之下检定结果',
    'strTQAAtOther': '【.tqa】指令\n代骰三尺之下检定结果',
    'strTQAHideShowAtOther': '【.tqa】指令\n暗代骰三尺之下检定提示',
    'strTQAHideAtOther': '【.tqa】指令\n暗代骰三尺之下检定结果',
    'strTQAError': '【.tqa】指令\n三尺之下检定错误',
    'strTQAFormatError': '【.tqa】指令\n格式错误',
    
    # .tqav 三尺之下对抗相关
    'strTQAVResult': '【.tqav】指令\n三尺之下对抗结果',
    'strTQAVError': '【.tqav】指令\n三尺之下对抗错误',
    'strTQAVNoAtError': '【.tqav】指令\n未@对方错误',
    'strTQAVFormatError': '【.tqav】指令\n格式错误',
    
    # 通用错误
    'strCoinRollError': '通用\n铜钱投掷错误',
    'strMyExprError': '通用\n自己表达式错误',
    'strOtherExprError': '通用\n对方表达式错误',
    'strAttrExprError': '通用\n属性表达式错误',
    'strDifficultyExprError': '通用\n难度表达式错误'
}

dictHelpDocTemp = {
    'sanchi': '''【三尺之下铜钱卦】
.tq(h)(b/p数字)(次数)#(铜钱数量或表达式)

参数说明：
- h：暗骰
- b/p数字：优势/劣势转换数量
- 次数：投掷次数（最多10次）
- 铜钱数量：3-100枚，支持表达式和技能名

例子：
.tq 5        # 投掷5枚铜钱
.tq b2 力量   # 2个优势转换，铜钱数量为力量技能值
.tq 3#p1 敏捷+5  # 3次投掷，1个劣势转换，每次投掷敏捷+5枚铜钱

【三尺之下检定】
.tqa(h)(b/p数字)(属性表达式)#(难度表达式)(@其他人)

检定规则：
- 难度 < 属性：1个阳爻成功（简单检定）
- 难度 = 属性：2个阳爻成功（标准检定）  
- 难度 > 属性，差值≤2：3个阳爻成功（困难检定）
- 难度 > 属性，差值>2：3个阳爻成功且自动增加劣势（极难检定）

例子：
.tqa 力量#15      # 力量检定，难度15
.tqa b1 敏捷+5#12 # 优势检定，敏捷+5对抗难度12
.tqa h 意志#困难 @张三  # 暗骰代骰意志检定

【三尺之下对抗】
.tqav(b/p数字)(自己属性)#(b/p数字)(对方属性)@对方

对抗规则：
- 双方各投3枚铜钱，计算阳爻数量
- 阳爻数量+属性值=最终对抗值
- 数值高者获胜，相等为平手

例子：
.tqav 力量#敏捷 @张三     # 自己力量对抗张三敏捷
.tqav b1 武艺+5#p1 剑法 @李四  # 优势武艺+5对抗李四劣势剑法''',
}