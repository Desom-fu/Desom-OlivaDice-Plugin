# -*- encoding: utf-8 -*-
'''
忍术释放模块的自定义回复
'''

import OlivOS
import OlivaDiceCore
import OlivaDiceLexNinjutsu

dictStrCustomDict = {}

dictStrCustom = {
    'strNinjutsuUpdateComplete': '忍术信息已更新，共 {tNinjutsuCount} 个忍术。',
    'strNinjutsuClearComplete': '忍术信息已清空。',
    'strNinjutsuNotFound': '未找到忍术。',
    'strNinjutsuNotFoundTrySearch': '未找到忍术，正在尝试搜索相关忍术……',
    'strNinjutsuInfo': '{tNinjutsuName}\n{tNinjutsuDescription}\n更多信息：{tNinjutsuUrl}',
    'strNinjutsuNoAudio': '该忍术暂无音频。',
    'strNinjutsuSearchNoResult': '未搜索到相关忍术。',
    'strNinjutsuSearchResultTitle': '找到以下相关忍术：',
    'strNinjutsuSearchResultItem': '\n·{tNinjutsuName}\n简介：{tNinjutsuDescription}',
    'strNinjutsuUpdateError': '更新忍术信息失败：{tError}',
    'strNinjutsuNetworkError': '网络请求失败：{tError}',
    'strNinjutsuDownloadStart': '开始下载全部忍术音频……\n共 {tTotalJutsu} 个忍术，预计需要一些时间',
    'strNinjutsuDownloadComplete': '下载完成！\n成功: {tSuccessCount} 个忍术\n失败: {tFailCount} 个忍术\n总音频: {tTotalAudio} 个\n保存位置: {tAudioDir}',
    'strNinjutsuDownloadError': '下载失败：{tError}',
    'strNinjutsuConfigInfo': '【忍术配置信息】\n匹配等级: {tMatchLevel}\n搜索结果上限: {tSearchLimit}\n描述预览字数: {tDescriptionPreviewLimit}',
    'strNinjutsuConfigInvalid': '配置参数无效，已恢复默认值。\n匹配等级: {tMatchLevel}\n搜索结果上限: {tSearchLimit}\n描述预览字数: {tDescriptionPreviewLimit}',
    # 配置参数（用户可修改，无法转换为int时使用默认值）
    'tMatchLevel': '1',  # 匹配等级: 0=严格, 1=忽略标点, 2=同音 (有pypinyin时默认2)
    'tSearchLimit': '10',  # 搜索结果上限
    'tDescriptionPreviewLimit': '50',  # 描述预览字数上限
}

dictStrConst = {
}

dictGValue = {
}

dictTValue = {
    'tNinjutsuCount': '0',
    'tNinjutsuName': '',
    'tNinjutsuDescription': '',
    'tNinjutsuUrl': '',
    'tError': '',
    'tTotalJutsu': '0',
    'tSuccessCount': '0',
    'tFailCount': '0',
    'tTotalAudio': '0',
    'tAudioDir': '',
    'tMatchLevel': '1',  # 仅用于显示，实际配置在 dictStrCustom 中
    'tSearchLimit': '10',  # 仅用于显示，实际配置在 dictStrCustom 中
    'tDescriptionPreviewLimit': '50',  # 仅用于显示，实际配置在 dictStrCustom 中
}

dictStrCustomNote = {
    'strNinjutsuUpdateComplete': '【忍术更新】命令\n更新完成提示',
    'strNinjutsuClearComplete': '【忍术清空】命令\n清空完成提示',
    'strNinjutsuNotFound': '【忍术】命令\n未找到忍术提示',
    'strNinjutsuNotFoundTrySearch': '【忍术】命令\n未找到忍术，尝试搜索提示',
    'strNinjutsuInfo': '【忍术信息】命令\n忍术信息显示',
    'strNinjutsuNoAudio': '【忍术释放】命令\n忍术无音频提示',
    'strNinjutsuSearchNoResult': '【忍术搜索】命令\n搜索无结果提示',
    'strNinjutsuSearchResultTitle': '【忍术搜索】命令\n搜索结果标题',
    'strNinjutsuSearchResultItem': '【忍术搜索】命令\n搜索结果单项',
    'strNinjutsuUpdateError': '【忍术更新】命令\n更新失败提示',
    'strNinjutsuNetworkError': '【忍术】命令\n网络错误提示',
    'strNinjutsuDownloadStart': '【忍术下载】命令\n下载开始提示',
    'strNinjutsuDownloadComplete': '【忍术下载】命令\n下载完成提示',
    'strNinjutsuDownloadError': '【忍术下载】命令\n下载失败提示',
    'strNinjutsuConfigInfo': '【忍术配置】命令\n配置信息显示',
    'strNinjutsuConfigInvalid': '【忍术配置】命令\n配置参数无效提示',
    'tMatchLevel': '【配置参数】匹配等级\n0=严格匹配, 1=忽略标点匹配, 2=同音匹配\n默认: 1 (有pypinyin时为2)',
    'tSearchLimit': '【配置参数】搜索结果上限\n默认: 10',
    'tDescriptionPreviewLimit': '【配置参数】描述预览字数上限\n默认: 50',
}

dictHelpDocTemp = {
    '忍术帮助': '''【忍术帮助】
握握手，握握双手。

.忍术 更新 - 从忍法帖更新忍术信息（需要权限）
.忍术 清空 - 清空当前忍术信息（需要权限）
.忍术 信息 <忍术名> - 获取忍术信息
.忍术 释放 <忍术名> - 释放忍术，播放忍术音频
.释放忍术 <忍术名> - 释放忍术，播放忍术音频
.忍术 搜索 <关键字> - 搜索相关忍术
.忍术 下载 - 下载全部忍术音频到本地（需要权限）
.忍术 配置 - 查看当前配置参数

示例：
.忍术 释放 握握手握握双手
.释放忍术 吓我一跳我释放忍术
.忍术 信息 岚刀一直切
.忍术 搜索 握手
.忍术 下载
.忍术 配置

特性：
- 自动忽略标点符号匹配
- 支持同音匹配（需安装 pypinyin 库）
- 数据持久化保存到本地
- 重启后自动加载历史数据
- 本地音频优先播放（需先下载）
- 使用 requests 库提供更稳定的下载（推荐安装）
- 支持通过回复词自定义配置参数

配置参数（在回复词中修改）：
- tMatchLevel: 匹配等级 (0=严格, 1=忽略标点, 2=同音)
  默认: 1 (如果安装了 pypinyin 则为 2)
- tSearchLimit: 搜索结果上限
  默认: 10
- tDescriptionPreviewLimit: 描述预览字数上限
  默认: 50

忍术数据来源：忍法帖 https://wsfrs.com/
数据存储位置：./plugin/data/OlivaDiceLexNinjutsu/
音频存储位置：./data/audios/OlivaDiceLexNinjutsu/''',
}
