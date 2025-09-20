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
    'strTQResult': '[{tName}]进行占卜，掷出{tNumber}枚铜钱，结果为: {tResult}\n阴: {tYinNumber}次；阳: {tYangNumber}次',
    'strTQResultMore': '[{tName}]进行占卜，掷了{tTime}次，每次掷出{tNumber}枚铜钱，结果为: \n{tResult}\n总和次数：阴: {tYinNumber}次；阳: {tYangNumber}次',
    'strTQError': '请输入1-100之间的数字进行占卜，例如: .tq3',
    'strTQHide': '[{tName}]在群({tGroupId})中进行暗中占卜：\n掷出{tNumber}枚铜钱，结果为: {tResult}\n阴: {tYinNumber}次；阳: {tYangNumber}次',
    'strTQHideShow': '[{tName}]进行暗中占卜',
    'strTQHideMore': '[{tName}]在群({tGroupId})中进行暗中占卜：\n掷了{tTime}次，每次掷出{tNumber}枚铜钱，结果为: \n{tResult}\n总和次数：阴: {tYinNumber}次；阳: {tYangNumber}次',
    'strTQHideShowMore': '[{tName}]进行暗中占卜',
    'strTQAtOther': '为[{tName}]进行占卜，掷出{tNumber}枚铜钱，结果为: {tResult}\n阴: {tYinNumber}次；阳: {tYangNumber}次',
    'strTQAtOtherMore': '为[{tName}]进行占卜，掷了{tTime}次，每次掷出{tNumber}枚铜钱，结果为: \n{tResult}\n总和次数：阴: {tYinNumber}次；阳: {tYangNumber}次',
    'strTQHideAtOther': '[{tName}]在群({tGroupId})中的暗中占卜结果：\n掷出{tNumber}枚铜钱，结果为: {tResult}\n阴: {tYinNumber}次；阳: {tYangNumber}次',
    'strTQHideShowAtOther': '为[{tName}]进行暗中占卜',
    'strTQHideAtOtherMore': '[{tName}]在群({tGroupId})中的暗中占卜结果：\n掷了{tTime}次，每次掷出{tNumber}枚铜钱，结果为: \n{tResult}\n总和次数：阴: {tYinNumber}次；阳: {tYangNumber}次',
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
.tq (h)(数字#)(数字) @其他人 进行阴阳投掷，若没有数值默认值为1
可进行多次投掷，# 前代表投掷的次数
添加h参数进行暗骰

管理员可以为他人进行代骰'''
}
