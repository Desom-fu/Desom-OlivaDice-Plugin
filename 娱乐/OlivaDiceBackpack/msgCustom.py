# -*- encoding: utf-8 -*-
'''
背包插件自定义回复内容
'''

import OlivOS
import OlivaDiceCore
import OlivaDiceBackpack

dictStrCustomDict = {}

dictStrCustom = {
    # 贡献值相关
    'strContributionQuery': '你的贡献值为: {tContribution}',
    'strContributionQueryOther': '[{tTargetName}]的贡献值为: {tContribution}',
    'strContributionAdd': '已为[{tTargetName}]增加[{tAmount}]贡献值，当前贡献值: {tContribution}',
    'strContributionReduce': '已为[{tTargetName}]减少[{tAmount}]贡献值，当前贡献值: {tContribution}',
    'strContributionDeduct': '已扣除[{tAmount}]贡献值，当前贡献值: {tContribution}',
    'strContributionInsufficient': '贡献值不足，需要[{tRequired}]，当前只有[{tCurrent}]',
    'strContributionNegative': '贡献值不能为负数',
    
    # 背包相关
    'strInventoryQuery': '你的背包:\n{tInventory}',
    'strInventoryQueryOther': '[{tTargetName}]的背包:\n{tInventory}',
    'strInventoryEmpty': '背包为空',
    'strInventoryEmptyOther': '[{tTargetName}]的背包为空',
    'strItemAdd': '已为[{tTargetName}]添加[{tItem}] x[{tAmount}]',
    'strItemRemove': '已为[{tTargetName}]移除[{tItem}] x[{tAmount}]',
    'strItemNotEnough': '[{tTargetName}]的[{tItem}]数量不足，当前只有[{tCurrent}]',
    'strItemNotExist': '[{tTargetName}]没有[{tItem}]',
    
    # 商店相关
    'strShopList': '商店商品:\n{tShopList}',
    'strShopEmpty': '商店暂无商品',
    'strPurchaseSuccess': '购买成功！获得[{tItem}] x [{tAmount}]，消耗贡献值: {tCost}',
    'strPurchaseFailed': '购买失败: {tReason}',
    'strItemNotInShop': '商品[{tItem}]不在商店中',
    
    # 道具使用相关
    'strItemUseSuccess': '使用[{tItem}]成功！',
    'strItemUseFailed': '使用[{tItem}]失败: {tReason}',
    'strItemNotUsable': '道具[{tItem}]无法使用',
    'strItemNotInInventory': '背包中没有[{tItem}]',
    
    # 盲盒相关
    'strBlindboxDraw': '你打开了[道具盲盒]，获得了：\n{tResult}',
    'strBlindboxDrawMultiple': '你连续打开了[{tCount}]个[道具盲盒]，结果如下:\n{tResult}',
    'strBlindboxNotEnough': '你的[道具盲盒]不足[{tCount}]个，无法进行{tType}！',
    'strBlindboxInvalidCommand': '[道具盲盒]只能单抽、五连或十连哦，具体指令如下: \n.use [道具盲盒](单抽/五连/十连)，默认为单抽。',
    'strBlindboxSimulation': '模拟一万连抽奖结果：\n{tResult}',
    'strBlindboxWeightError': '盲盒配置错误：总概率为[{tTotal}%]，应为100%',
    
    # 权限相关
    'strPermissionDenied': '权限不足，需要管理员或骰主权限',
    'strNoTarget': '未找到目标用户，请@目标用户',
    'strInvalidAmount': '数量必须为正整数',
    'strInvalidCommand': '命令格式错误',
    'strPermissionGranted': '已授予[{tTargetName}]背包管理权限',
    'strPermissionRevoked': '已撤销[{tTargetName}]的背包管理权限',
    'strPermissionList': '当前拥有背包管理权限的用户：\n{tAdminList}',
    'strPermissionListEmpty': '当前没有用户拥有背包管理权限',
    'strOnlyMasterCanGrant': '只有骰主可以授予或撤销权限',
    
    # 全体操作相关
    'strGlobalItemAdd': '已为全体成员发放[{tItem}] x [{tAmount}]',
    'strGlobalItemRemove': '已为全体成员移除[{tItem}] x [{tAmount}]',
    'strGlobalItemRemoveSkip': '已为全体成员移除[{tItem}] x [{tAmount}]，跳过[{tSkipCount}]个没有该物品的成员',
}

dictStrConst = {
}

dictGValue = {
}

dictTValue = {
    'tContribution': '0',
    'tTargetName': '用户',
    'tAmount': '1',
    'tItem': '物品',
    'tInventory': '无物品',
    'tShopList': '无商品',
    'tCost': '0',
    'tReason': '未知错误',
    'tResult': '',
    'tCount': '1',
    'tType': '单抽',
    'tTotal': '0',
    'tCurrent': '0',
    'tRequired': '0',
    'tSkipCount': '0',
    'tAdminList': '无',
}

dictStrCustomNote = {
    'strContributionQuery': '【贡献值查询】命令\n查询自己贡献值时的回复',
    'strContributionQueryOther': '【贡献值查询】命令\n查询他人贡献值时的回复',
    'strContributionAdd': '【贡献值增加】命令\n增加他人贡献值时的回复',
    'strContributionReduce': '【贡献值减少】命令\n减少他人贡献值时的回复',
    'strContributionDeduct': '【贡献值扣除】命令\n扣除自己贡献值时的回复',
    'strContributionInsufficient': '【贡献值不足】错误\n贡献值不足时的回复',
    'strContributionNegative': '【贡献值负数】错误\n贡献值为负数时的回复',
    'strInventoryQuery': '【背包查询】命令\n查询自己背包时的回复',
    'strInventoryQueryOther': '【背包查询】命令\n查询他人背包时的回复',
    'strInventoryEmpty': '【背包查询】命令\n自己背包为空时的回复',
    'strInventoryEmptyOther': '【背包查询】命令\n他人背包为空时的回复',
    'strItemAdd': '【物品添加】命令\n添加物品时的回复',
    'strItemRemove': '【物品移除】命令\n移除物品时的回复',
    'strItemNotEnough': '【物品不足】错误\n物品数量不足时的回复',
    'strItemNotExist': '【物品不存在】错误\n物品不存在时的回复',
    'strShopList': '【商店查询】命令\n查询商店时的回复',
    'strShopEmpty': '【商店查询】命令\n商店为空时的回复',
    'strPurchaseSuccess': '【购买商品】命令\n购买成功时的回复',
    'strPurchaseFailed': '【购买商品】命令\n购买失败时的回复',
    'strItemNotInShop': '【商品不存在】错误\n商品不在商店时的回复',
    'strItemUseSuccess': '【使用道具】命令\n使用道具成功时的回复',
    'strItemUseFailed': '【使用道具】命令\n使用道具失败时的回复',
    'strItemNotUsable': '【道具不可用】错误\n道具无法使用时的回复',
    'strItemNotInInventory': '【道具不存在】错误\n背包中没有道具时的回复',
    'strBlindboxDraw': '【盲盒单抽】命令\n单抽盲盒时的回复',
    'strBlindboxDrawMultiple': '【盲盒连抽】命令\n连抽盲盒时的回复',
    'strBlindboxNotEnough': '【盲盒不足】错误\n盲盒数量不足时的回复',
    'strBlindboxInvalidCommand': '【盲盒命令错误】错误\n盲盒命令格式错误时的回复',
    'strBlindboxSimulation': '【盲盒模拟】命令\n模拟一万连时的回复',
    'strBlindboxWeightError': '【盲盒配置错误】错误\n盲盒概率配置错误时的回复',
    'strPermissionDenied': '【权限不足】错误\n权限不足时的回复',
    'strNoTarget': '【未找到目标】错误\n未找到目标用户时的回复',
    'strInvalidAmount': '【数量无效】错误\n数量无效时的回复',
    'strInvalidCommand': '【命令无效】错误\n命令格式错误时的回复',
    'strGlobalItemAdd': '【全体发放】命令\n全体发放物品时的回复',
    'strGlobalItemRemove': '【全体移除】命令\n全体移除物品时的回复',
    'strGlobalItemRemoveSkip': '【全体移除】命令\n全体移除物品时跳过部分成员的回复',
    'strPermissionGranted': '【授予权限】命令\n授予权限成功时的回复',
    'strPermissionRevoked': '【撤销权限】命令\n撤销权限成功时的回复',
    'strPermissionList': '【权限列表】命令\n查看权限列表时的回复',
    'strPermissionListEmpty': '【权限列表】命令\n权限列表为空时的回复',
    'strOnlyMasterCanGrant': '【权限不足】错误\n只有骰主可以授予或撤销权限',
}

dictHelpDocTemp = {
    'bag': '''【背包系统】
(-) .bag 贡献值 - 查询自己的贡献值
(+) .bag 贡献值 [@某人] - 查询他人的贡献值
(+) .bag 贡献值 增加/减少 [数量] [@某人] - 为某人增加/减少贡献值
(-) .bag 贡献值 扣除 [数量] - 扣除自己的贡献值
(-) .bag 背包 - 查询自己的背包
(+) .bag 背包 [@某人] - 查询他人的背包
(+) .bag 背包 添加/删除 [物品名] [数量] [@某人] - 为某人添加/删除物品
(+) .bag 背包 全体发放/删除 [物品名] [数量] - 为全体成员发放/删除物品
(-) .bag 商店 - 查看商店商品
(-) .bag 购买 [物品名] [数量] - 购买商品
(-) .bag 使用 [物品名] [参数] - 使用道具
(-) .bag 使用 道具盲盒 [单抽/五连/十连] - 使用道具盲盒(默认单抽)
(^) .bag 权限 授予 [@某人] - 授予某人背包管理权限
(^) .bag 权限 撤销 [@某人] - 撤销某人的背包管理权限
(^) .bag 权限 列表 - 查看拥有权限的用户列表

命令标识说明：
(+)用户需要管理员/群主/骰主/授权用户权限
(^)仅骰主可用
(-)普通用户可用''',
}
