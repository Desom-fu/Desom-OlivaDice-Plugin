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
    'strTQResult': '[{tName}]进行占卜{tExprShow}，掷出{tOriginalNumber}枚铜钱{tExtraCoinsText}，结果为: {tResult}\n阴: {tYinNumber}次；阳: {tYangNumber}次{tTransformText}',
    'strTQResultMore': '[{tName}]进行占卜{tExprShow}，掷了{tTime}次，每次掷出{tOriginalNumber}枚铜钱{tAllExtraCoinsText}，结果为: \n{tResult}\n总和次数：阴: {tYinNumber}次；阳: {tYangNumber}次{tBPText}',
    'strTQError': '请输入正确的表达式或数字进行占卜，例如: .tq3 或 .tqb2+5',
    'strTQHide': '[{tName}]在群({tGroupId})中进行暗中占卜{tExprShow}：\n掷出{tOriginalNumber}枚铜钱{tExtraCoinsText}，结果为: {tResult}\n阴: {tYinNumber}次；阳: {tYangNumber}次{tTransformText}',
    'strTQHideShow': '[{tName}]进行暗中占卜',
    'strTQHideMore': '[{tName}]在群({tGroupId})中进行暗中占卜{tExprShow}：\n掷了{tTime}次，每次掷出{tOriginalNumber}枚铜钱{tAllExtraCoinsText}，结果为: \n{tResult}\n总和次数：阴: {tYinNumber}次；阳: {tYangNumber}次{tBPText}',
    'strTQHideShowMore': '[{tName}]进行暗中占卜',
    'strTQAtOther': '为[{tName}]进行占卜{tExprShow}，掷出{tOriginalNumber}枚铜钱{tExtraCoinsText}，结果为: {tResult}\n阴: {tYinNumber}次；阳: {tYangNumber}次{tTransformText}',
    'strTQAtOtherMore': '为[{tName}]进行占卜{tExprShow}，掷了{tTime}次，每次掷出{tOriginalNumber}枚铜钱{tAllExtraCoinsText}，结果为: \n{tResult}\n总和次数：阴: {tYinNumber}次；阳: {tYangNumber}次{tBPText}',
    'strTQHideAtOther': '[{tName}]在群({tGroupId})中的暗中占卜结果{tExprShow}：\n掷出{tOriginalNumber}枚铜钱{tExtraCoinsText}，结果为: {tResult}\n阴: {tYinNumber}次；阳: {tYangNumber}次{tTransformText}',
    'strTQHideShowAtOther': '为[{tName}]进行暗中占卜',
    'strTQHideAtOtherMore': '[{tName}]在群({tGroupId})中的暗中占卜结果{tExprShow}：\n掷了{tTime}次，每次掷出{tOriginalNumber}枚铜钱{tAllExtraCoinsText}，结果为: \n{tResult}\n总和次数：阴: {tYinNumber}次；阳: {tYangNumber}次{tBPText}',
    'strTQHideShowAtOtherMore': '为[{tName}]进行暗中占卜'
}

dictStrConst = {
}

dictGValue = {
}

dictStrCustomNote = {
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
    'strTQHideShowAtOtherMore': '【.tq】指令\n暗骰代骰多次占卜提示'
}

dictTValue = {}

dictHelpDocTemp = {
    'tq': '''【阴阳投掷】
.tq (h)(b数字)(p数字)(次数#)(表达式|数字) @其他人 进行阴阳投掷
支持表达式和技能解析，例如：.tq3 或 .tq敏捷+5
支持b/p转换：
- b/b数字：将阴转换为阳（b2表示转换2个）
- p/p数字：将阳转换为阴并增加铜钱（p2表示转换2个）
可进行多次投掷，# 前代表投掷的次数
添加h参数进行暗骰

管理员可以为他人进行代骰

示例：
.tq5 - 掷5枚铜钱
.tqb3+2 - 掷3+2枚铜钱，将1个阴转换为阳
.tqp2b1+敏捷 - 掷敏捷值枚铜钱，转换2个阳为阴、1个阴为阳
.tq3#5 - 投掷3次，每次5枚铜钱'''
}
