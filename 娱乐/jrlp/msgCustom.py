# -*- encoding: utf-8 -*-
'''
这里写你的自定义回复
'''

import OlivOS
import OlivaDiceCore
import jrlp

dictStrCustomDict = {}

dictStrCustom = {
    'jrlpFirst': '让小芙瞧瞧，[{tUserName}]今天的群老婆是：\n{name}({qq})',
    'jrlpRepeat': '[{tUserName}]今天已经有老婆啦，不要太贪心哦！\n你的今日老婆是：{name}({qq})',
    'jrlpRobot': '让小芙瞧瞧，[{tUserName}]今天的群老婆是：\n{name}({qq})\n哇，你抽到了小芙！今天小芙就是你的老婆了~',
    'jrlpSelf': '让小芙瞧瞧，[{tUserName}]今天的群老婆是：\n{name}({qq})\n哇，你的今日老婆居然是自己诶！'
}

dictStrConst = {
}

dictGValue = {
}

dictTValue = {
}

dictStrCustomNote = {
    'jrlpFirst': '【今日老婆】\n首次抽取今日老婆',
    'jrlpRepeat': '【今日老婆】\n重复查看今日老婆',
    'jrlpSelf': '【今日老婆】\n抽到自己',
    'jrlpRobot': '【今日老婆】\n抽到机器人自己'
}

dictHelpDocTemp = {
    '今日老婆': '''【今日老婆帮助】
查看今天的群老婆，
每日只能抽取一次，重复使用将显示同一个人。'''
}