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
import OlivaDiceTaichi

dictStrCustomDict = {}

dictStrCustom = {
    'strTQResult': '[{tName}]进行占卜，掷出{tNumber}枚铜钱，结果为: {tResult}\n阴: {tYinNumber}次；阳: {tYangNumber}次',
    'strTQResultMore': '[{tName}]进行占卜，掷了{tTime}次，每次掷出{tNumber}枚铜钱，结果为: \n{tResult}\n总和次数：阴: {tYinNumber}次；阳: {tYangNumber}次',
    'strTQError': '请输入1-100之间的数字进行占卜，例如: .tq3'
}

dictStrConst = {
}

dictGValue = {
}

dictStrCustomNote = {
    'strTQResult': '【.tq】指令\n占卜结果',
    'strTQResultMore': '【.tq】指令\n多次占卜结果',
    'strTQError': '【.tq】指令\n占卜错误'
}

dictTValue = {}

dictHelpDocTemp = {
    'tq': '''【阴阳投掷】
.tq (数字#)(数字) 进行阴阳投掷，若没有数值默认值为1
可进行多次投掷，# 前代表投掷的次数'''
}
