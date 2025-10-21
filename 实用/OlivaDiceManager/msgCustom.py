# -*- encoding: utf-8 -*-
'''
自定义回复内容
'''

import OlivOS
import OlivaDiceCore
import OlivaDiceManager

dictStrCustomDict = {}

dictStrCustom = {
    'strGroupNameSetSuccess': '群名设置成功！',
    'strGroupNameSetFailed': '群名设置失败，请检查Bot权限',
    'strAdminSetSuccess': '已将[{tTargetName}]设置为管理员！',
    'strAdminSetFailed': '设置[{tTargetName}]为管理员失败,请检查Bot权限',
    'strAdminRemoveSuccess': '已取消[{tTargetName}]的管理员权限！',
    'strAdminRemoveFailed': '取消[{tTargetName}]的管理员权限失败,请检查Bot权限',
    'strAdminParamError': '请指定[添加]或[移除]',
    'strGroupBanSuccess': '全员禁言设置成功！',
    'strGroupBanFailed': '全员禁言设置失败，请检查Bot权限',
    'strGroupBanParamError': '请指定[开启]或[关闭]',
    'strKickSuccess': '已将[{tTargetName}]踢出群聊！',
    'strKickFailed': '踢出[{tTargetName}]失败，请检查Bot权限',
    'strLikeSuccess': '已为[{tTargetName}]点赞[{tContent}]次！请确认对方添加Bot为好友以确保点赞生效',
    'strLikeSelfSuccess': '点赞自己[{tContent}]次成功！请先添加Bot为好友以确保点赞生效',
    'strLikeFailed': '点赞[{tTargetName}]失败，请检查Bot权限',
    'strCardSetSuccess': '已将[{tTargetName}]的群名片设置为:[{tContent}]',
    'strCardSetFailed': '设置[{tTargetName}]的群名片失败,请检查Bot权限',
    'strTitleSetSuccess': '已将[{tTargetName}]的群头衔设置为:[{tContent}]',
    'strTitleSetFailed': '设置[{tTargetName}]的群头衔失败，请检查Bot权限',
    'strTitleRemoveSuccess': '已取消[{tTargetName}]的群头衔！',
    'strTitleRemoveFailed': '取消[{tTargetName}]的群头衔失败，请检查Bot权限',
    'strBanSuccess': '已禁言[{tTargetName}] [{tContent}]秒！',
    'strBanFailed': '禁言[{tTargetName}]失败，请检查Bot权限',
    'strUnbanSuccess': '已解除[{tTargetName}]的禁言！',
    'strUnbanFailed': '解除[{tTargetName}]的禁言失败，请检查Bot权限',
    'strNoticeSuccess': '群公告发布成功！',
    'strNoticeFailed': '群公告发布失败，请检查Bot权限',
    'strNoTarget': '未找到目标用户，请@目标用户',
    'strNoContent': '内容不能为空',
}

dictStrConst = {
}

dictGValue = {
}

dictTValue = {
    'tTargetName': '用户',
}

dictStrCustomNote = {
    'strGroupNameSetSuccess': '【设置群名】命令\n群名设置成功时的回复',
    'strGroupNameSetFailed': '【设置群名】命令\n群名设置失败时的回复',
    'strAdminSetSuccess': '【设置管理员】命令\n管理员设置成功时的回复 ',
    'strAdminSetFailed': '【设置管理员】命令\n管理员设置失败时的回复 ',
    'strAdminRemoveSuccess': '【设置管理员】命令\n取消管理员成功时的回复 ',
    'strAdminRemoveFailed': '【设置管理员】命令\n取消管理员失败时的回复 ',
    'strAdminParamError': '【设置管理员】命令\n参数错误时的回复',
    'strGroupBanSuccess': '【全员禁言】命令\n全员禁言设置成功时的回复',
    'strGroupBanFailed': '【全员禁言】命令\n全员禁言设置失败时的回复',
    'strGroupBanParamError': '【全员禁言】命令\n参数错误时的回复',
    'strKickSuccess': '【踢出】命令\n踢出成功时的回复 ',
    'strKickFailed': '【踢出】命令\n踢出失败时的回复 ',
    'strLikeSuccess': '【点赞】命令\n点赞他人成功时的回复 ',
    'strLikeSelfSuccess': '【点赞】命令\n点赞自己成功时的回复',
    'strLikeFailed': '【点赞】命令\n点赞失败时的回复 ',
    'strCardSetSuccess': '【设置名片】命令\n群名片设置成功时的回复 ',
    'strCardSetFailed': '【设置名片】命令\n群名片设置失败时的回复 ',
    'strTitleSetSuccess': '【设置头衔】命令\n群头衔设置成功时的回复 ',
    'strTitleSetFailed': '【设置头衔】命令\n群头衔设置失败时的回复 ',
    'strTitleRemoveSuccess': '【取消头衔】命令\n取消头衔成功时的回复 ',
    'strTitleRemoveFailed': '【取消头衔】命令\n取消头衔失败时的回复 ',
    'strBanSuccess': '【禁言】命令\n禁言成功时的回复 ',
    'strBanFailed': '【禁言】命令\n禁言失败时的回复 ',
    'strUnbanSuccess': '【取消禁言】命令\n取消禁言成功时的回复 ',
    'strUnbanFailed': '【取消禁言】命令\n取消禁言失败时的回复 ',
    'strNoticeSuccess': '【群公告】命令\n群公告发布成功时的回复',
    'strNoticeFailed': '【群公告】命令\n群公告发布失败时的回复',
    'strNoTarget': '未找到目标用户时的回复',
    'strNoContent': '内容为空时的回复',
}

dictHelpDocTemp = {
    '群管': '''【群管功能】
(-/*) .设置 名片 [内容] [@某人/自己] - 设置群名片(用户给他人设置需要权限，设置自己不需要)
(+/*) .设置 群名 [群名] - 设置群名称
(+/*) .设置 管理员 [添加/移除] [@某人] - 添加/移除某人的管理员权限
(+/*) .设置 头衔 [内容] [@某人/自己] - 设置群头衔(没有指定对象时默认自己。)
(+/*) .设置 公告 [内容] - 发布群公告
(+/*) .全员禁言 [开启/关闭] - 开启/关闭全员禁言
(+/*) .禁言 [时长(秒)] [@某人] - 禁言群成员，默认1800秒
(+/*) .取消 头衔 [@某人/自己] - 取消群头衔(没有指定对象时默认自己。注：此命令需要机器人拥有群主权限
(+/*) .取消 禁言 [@某人] - 解除群成员禁言
(+/*) .踢出 [@某人] - 踢出群成员
(-) .点赞 [次数] [@某人/自己] - 点赞，默认20次(用户点赞他人需要权限，没有指定对象时默认自己，请先添加Bot为好友)

命令标识说明：
(+)用户需要管理员/群主/骰主权限
(*)机器人需要管理员/群主权限
(-)部分功能需要用户具有权限，部分不需要''',
}
