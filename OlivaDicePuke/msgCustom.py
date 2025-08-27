# -*- encoding: utf-8 -*-
'''
@File      :   msgCustom.py
@Author    :   Desom-fu
@Contact   :   Desom233@outlook.com
@License   :   AGPL
@Copyright :   (C) 2020-2021, OlivOS-Team
@Desc      :   None
'''

import OlivOS
import OlivaDiceCore
import OlivaDicePuke

dictStrCustomDict = {}

# 扑克牌功能回复文本
dictStrCustom = {
    'strPukeDraw': '[{tName}]抽出了 {tDrawCount} 张牌，获得了: \n{tDrawnCards}。',
    'strPukeDrawError': '抽牌失败！你想抽的牌({tDrawCount}张)比牌堆里剩下的({tDeckCount}张)还多。',
    'strPukeDeckEmpty': '你的牌堆已经空了，请使用 .puke reset 重置。',
    'strPukeInvalidNumber': '请输入一个有效的抽牌数量，例如: .puke 5',
    'strPukeReset': '[{tName}]的牌堆、随机池和手牌已经重置，现在是全新的54张牌了。',
    'strPukeShowSuit': '[{tName}]的持有手牌如下:\n{tHandCards}',
    'strPukeShowEmpty': '无',
    'strPukeDeckHeader': '[{tName}]的剩余牌堆详情如下({tDeckCount}张):',
    'strPukeDeckSuit': '\n{tSuit}：{tCards}',
    'strPukeDrawSpecific': '[{tName}]尝试抽取指定牌: {tCardsToDraw}\n结果: {tDrawnCards} 已放入手牌。\n剩余牌堆: {tDeckCount}张。',
    'strPukeDrawSpecificNotFound': '指定的牌 {tCardsToDraw} 不在牌堆中。',
    'strPukeDrawSpecificPartial': '[{tName}]尝试抽取指定牌: {tCardsToDraw}\n成功抽取并放入手牌: {tDrawnCards}\n未找到的牌: {tNotFoundCards}\n剩余牌堆: {tDeckCount}张。',
    'strPukeInvalidCard': '无效的牌名: {tInvalidCard}。可用花色: 黑桃、红心(红桃)、梅花(草花)、方片；大小王。',
    'strPukeAddCard': '[{tName}]将牌 {tAddedCards} 放入了手牌。\n剩余牌堆: {tDeckCount}张。',
    'strPukeAddCardNotFound': '指定的牌 {tCardsToAdd} 不在牌堆中，无法添加到手牌。',
    'strPukeAddCardPartial': '[{tName}]成功添加 {tAddedCards} 到手牌，但未找到 {tNotFoundCards}。\n剩余牌堆: {tDeckCount}张。',
    'strPukeAddCardDuplicate': '牌 {tDuplicateCards} 已经在随机池中，无法重复添加。',
    'strPukeEnd': '[{tName}]结束了本轮抽牌，随机池已清空，手牌已重新加入牌堆。',
    'strPukeClr': '[{tName}]的随机池和手牌已清空。',
    'strPukeRandomPoolHeader': '[{tName}]的随机池中的牌:',
    'strPukeRandomPoolEmpty': '随机池为空',
    'strPukeCheck': '[{tName}]的牌况如下：\n手牌: {tHandCards}\n随机池: {tRandomPool}',
    'strPukeChangeSuccess': '[{tName}]已将手牌 {tHandCard} 与牌库 {tDeckCard} 交换。',
    'strPukeChangeNotInHand': '你的手牌中没有 {tHandCard}，无法交换。',
    'strPukeChangeNotInDeck': '牌库中没有 {tDeckCard}，无法交换。',
    'strPukeRemoveCard': '[{tName}]已将 {tRemovedCards} 放回牌堆。剩余牌堆: {tDeckCount}张。',
    'strPukeRemoveCardNotInHand': '你手牌中没有这些牌: {tCardsToRemove}，无法移除。剩余牌堆: {tDeckCount}张。',
    'strPukeRemoveCardPartial': '成功移除: {tRemovedCards}，但未找到: {tNotInHand}。剩余牌堆: {tDeckCount}张。',
    'strPukeAddCardNeedSpecify': '请指定要添加的牌名，例如: .puke add 红心5',
    'strPukeRemoveCardNeedSpecify': '请指定要移除的牌名，例如: .puke rm 红心5',
    'strPukeChangeNeedSpecify': '请指定要交换的两张牌，例如: .puke change 红心5 黑桃A',
}

dictStrConst = {
}

dictGValue = {
}

# GUI备注（如有）
dictStrCustomNote = {
    'strPukeDraw': '【.puke】指令\n抽牌结果',
    'strPukeDrawError': '【.puke】指令\n抽牌数量错误',
    'strPukeDeckEmpty': '【.puke】指令\n牌堆为空',
    'strPukeInvalidNumber': '【.puke】指令\n无效数字',
    'strPukeReset': '【.puke reset】指令\n重置成功',
    'strPukeShowSuit': '【.puke hand】指令\n手牌展示',
    'strPukeShowEmpty': '【.puke hand】指令\n手牌为空',
    'strPukeDeckHeader': '【.puke deck】指令\n牌堆详情',
    'strPukeDeckSuit': '【.puke deck】指令\n牌堆花色分组',
    'strPukeDrawSpecific': '【.puke】指令\n指定抽牌成功',
    'strPukeDrawSpecificNotFound': '【.puke】指令\n指定抽牌未找到',
    'strPukeDrawSpecificPartial': '【.puke】指令\n部分指定抽牌成功',
    'strPukeInvalidCard': '【.puke】指令\n无效牌名',
    'strPukeAddCard': '【.puke add】指令\n添加牌到手牌',
    'strPukeAddCardNotFound': '【.puke add】指令\n添加牌未找到',
    'strPukeAddCardPartial': '【.puke add】指令\n部分添加牌成功',
    'strPukeAddCardDuplicate': '【.puke add】指令\n添加重复牌',
    'strPukeEnd': '【.puke end】指令\n结束本轮抽牌',
    'strPukeClr': '【.puke clr】指令\n清空随机池和手牌',
    'strPukeRandomPoolHeader': '【.puke pool】指令\n随机池展示',
    'strPukeRandomPoolEmpty': '【.puke pool】指令\n随机池为空',
    'strPukeCheck': '【.puke ck】指令\n查看手牌和随机池',
    'strPukeChangeSuccess': '【.puke change】指令\n手牌与牌库交换成功',
    'strPukeChangeNotInHand': '【.puke change】指令\n手牌中没有指定牌',
    'strPukeChangeNotInDeck': '【.puke change】指令\n牌库中没有指定牌',
    'strPukeRemoveCard': '【.puke rm】指令\n移除手牌到牌堆',
    'strPukeRemoveCardNotInHand': '【.puke rm】指令\n手牌中没有指定牌',
    'strPukeRemoveCardPartial': '【.puke rm】指令\n部分移除成功',
    'strPukeAddCardNeedSpecify': '【.puke add】指令\n未指定添加牌名',
    'strPukeRemoveCardNeedSpecify': '【.puke rm】指令\n未指定移除牌名',
    'strPukeChangeNeedSpecify': '【.puke change】指令\n未指定两张牌',
}

dictTValue = {}

# 帮助文档
dictHelpDocTemp = {
    'puke': '''【扑克牌】
.puke (数字) - 从你的个人牌堆中抽取指定数量的牌(默认为5)放入随机池。
.puke (牌名) - 抽取指定的牌(如: .puke 红心5 梅花3 小王 大王 黑桃K)放入手牌。
.puke show - 展示你当前持有的全部手牌(分类显示)。
.puke ck - 同时查看手牌和随机池中的牌。
.puke deck - 查看当前牌堆中剩余的牌。
.puke pool - 查看随机池中的牌。
.puke add (牌名) - 将指定牌放入手牌(如: .puke add 红心5)。
.puke rm (牌名) - 将指定的手牌放回牌堆(如: .puke rm 红心5)。
.puke clr - 清空随机池和手牌。
.puke end - 结束本轮抽牌，清空随机池并将手牌重新加入牌堆。
.puke reset - 重置你的个人牌堆和手牌。'''
}