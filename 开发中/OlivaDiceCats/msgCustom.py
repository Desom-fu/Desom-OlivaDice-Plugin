# -*- encoding: utf-8 -*-
'''
这里写你的自定义回复
'''

import OlivOS
import OlivaDiceCore
import OlivaDiceCats

dictStrCustomDict = {}

dictStrCustom = {
    'strCatsResult': '[{tName}]进行喵影奇谋检定{tChallengeTarget}\n{tRerollInfo}出值: {tFrontResult}+{tLuckDiceResult}={tTotalResult}\n挑战难度: {tBackResult} {tSkillCheckReasult}\n{tSuccessLevel}',
    'strCatsLuckDice': '幸运骰({tLuckValue}个): {tLuckDiceList}\n请选择1-{tLuckValue}：',
    'strCatsError': '喵影奇谋检定错误: {tResult}\n正确格式: .cats 前式#挑战难度@其他人（可选）',
    'strCatsInvalidSelection': '无效选择，请输入正确数字，请重新投掷',
    'strCatsTimeout': '选择超时，检定取消，请重新投掷',
    'strCatsSuccessLevel': '成功等级: {tSuccessLevelInt}'
}

dictStrConst = {
}

dictGValue = {
}

dictTValue = {
    'tFrontResult': '0',
    'tLuckDiceResult': '0',  
    'tTotalResult': '0',
    'tBackResult': '0',
    'tSkillCheckReasult': '',
    'tSuccessLevel': '',
    'tSuccessLevelInt': '0',
    'tLuckValue': '1',
    'tLuckDiceList': '',
    'tRerollInfo': '',
    'tResult': '',
    'tChallengeTarget': ''
}

dictStrCustomNote = {
    'strTemple': '【temple】命令\n这里写自定义回复对应的说明',
    'strCatsResult': '【.cats】指令\n进行喵影奇谋检定，显示挑战目标',
    'strCatsLuckDice': '【.cats】指令\n显示幸运骰并等待选择',
    'strCatsError': '【.cats】指令\n检定错误',
    'strCatsInvalidSelection': '【.cats】指令\n无效选择提示',
    'strCatsTimeout': '【.cats】指令\n选择超时提示',
    'strCatsSuccessLevel': '【.cats】指令\n成功等级'
}

dictHelpDocTemp = {
    'cats': '''【喵影奇谋检定】
.cats (b/p数字)(u/d数字)前式#(b/p数字)(u/d数字)(挑战难度)(@其他人)

参数说明：
- 前式：可以是数字或表达式，如10、2d6+10等
- 挑战难度：目标数值或表达式
- @其他人：可选，后式使用他人人物卡中的技能值（需要权限）
- b/p数字：加减最后的成功等级  
- u/d数字：加减幸运骰的数目（最多5个最少1个）

例子：
.cats u1 皮毛+1#10

检定规则：
1. 根据人物卡幸运属性投掷1-5个d10
2. 选择其中一个d10的结果
3. 前式+选择的d10结果与挑战难度对比
4. 大成功：连续投出10，幸运+1，点数+1
5. 大失败：连续投出1，幸运-1，点数+1
6. 若无挑战难度，则默认为10''',
}
