# -*- encoding: utf-8 -*-
'''
自定义回复模板
'''

import OlivOS
import OlivaDiceCore
import qianliexian

dictStrCustomDict = {}

dictStrCustom = {
    'strQlxEmpty': '请在。电后面输入文字哦！例如:。电 电所有人前列腺',
    'strQlxTooLong': '文字过长啦！最多支持10个字(20个字符)哦~（空格不算字符哦）',
    'strQlxNoBase': '错误:底图不存在，请将底图放置在 plugin/data/image/qianliexian/ 路径下',
    'strQlxError': '生成图片失败: {tError}'
}

dictStrConst = {
}

dictGValue = {
}

dictTValue = {
}

dictStrCustomNote = {
    'strQlxEmpty': '【。电】指令\n未输入文字时的提示',
    'strQlxTooLong': '【。电】指令\n文字过长时的提示',
    'strQlxNoBase': '【。电】指令\n底图不存在时的提示',
    'strQlxError': '【。电】指令\n生成图片失败时的提示'
}

dictHelpDocTemp = {
    '电所有人前列腺': '''【电所有人前列腺】
使用命令: 。电[文字内容]

功能说明：
生成"电所有人前列腺"风格的表情包图片

使用示例：
• .电电所有人前列腺
• .电今天天气真好
• .电大家早上好

注意事项：
• 最多支持15个汉字(30个字符)
• 需要在指定路径放置底图文件
• 自动管理临时图片文件''',
}
