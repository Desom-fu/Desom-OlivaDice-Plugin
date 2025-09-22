import io
import re

import requests
from PIL import Image as IMG
from PIL import ImageOps, ImageDraw # 导入 ImageDraw 模块

from . import basic_libs, settings

import OlivaDiceCore
import OlivOS

def make_frame(avatar, i, squish=0, flip=False):
    spec = list(settings.frame_spec[i])
    for j, s in enumerate(spec):
        spec[j] = int(s + settings.squish_factor[i][j] * squish)
    hand = IMG.open(settings.frames[i])
    if flip:
        avatar = ImageOps.mirror(avatar)
    avatar = avatar.resize(
        (
            int((spec[2] - spec[0]) * 1.6),
            int((spec[3] - spec[1]) * 1.6)
        ),
        IMG.Resampling.LANCZOS
    )
    # 并贴到空图像上
    gif_frame = IMG.new('RGB', (112, 112), (255, 255, 255))
    # 注意：这里的 paste 方法会利用 avatar 的透明通道
    gif_frame.paste(avatar, (spec[0]-10, spec[1]-15), avatar)
    # 将手覆盖（包括偏移量）
    gif_frame.paste(
        hand, (0, int(squish * settings.squish_translation_factor[i])-10), hand)
    return gif_frame


def save_gif(gif_frames, dest, fps=10):
    # 使用 PIL 保存 GIF
    gif_frames[0].save(
        dest,
        save_all=True,
        append_images=gif_frames[1:],
        duration=int(1000 / fps),  # 持续时间以毫秒为单位
        loop=0  # 0 表示永远循环
    )


def petpet(member_id, flip=False, squish=0, fps=20):

    file_path = basic_libs.Path.join([settings.PIC_PATH] , False)
    pic_name = settings.output_pic_name.format(member_id=member_id)
    res = f"[CQ:image,file={basic_libs.Path.join([settings.PIC_PATH[-2:]] , False)}\{pic_name}]"
    if basic_libs.Path.isexit(f"{file_path}\{pic_name}"):
        return res
    url = settings.url.format(
        member_id=member_id
    )
    response = requests.get(url=url)
    if response.status_code == 200:
        # 直接将响应内容传递给Image.open（这里假设响应内容是图像数据
        avatar = IMG.open(io.BytesIO(response.content))
    else:
        # 处理请求失败的情况
        print(f"Failed to retrieve image, status code: {response.status_code}")
        avatar = None  # 或者你可以设置一个默认图像或其他错误处理逻辑
        return False
        
    # 确保图像为 RGBA 模式，以支持透明度
    avatar = avatar.convert("RGBA")
    size = avatar.size
    
    # 创建一个黑色的圆形蒙版
    mask = IMG.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    # 在蒙版上画一个白色的填充圆形
    draw.ellipse((0, 0) + size, fill=255)
    
    # 将蒙版应用到头像的 alpha 通道
    avatar.putalpha(mask)

    gif_frames = []
    for i in range(5):
        gif_frames.append(make_frame(avatar, i, squish=squish, flip=flip))
    save_gif(gif_frames, f'{file_path}\{pic_name}', fps=fps)
    return res


def checkpetpet(retext, check_text):
    match = re.search(retext, check_text)
    if match:
        # 优先返回第一个分组（CQ码形式），如果没有则返回第二个分组（纯数字形式）
        return match.group(1) or match.group(2)
    else:
        return False


def basic_init():
    basic_libs.Path.create_folder(settings.PIC_PATH, False)


def pg_main(plugin_event):
    """主函数

    Arguments:
        plugin_event {_type_} -- 不言自明

    Returns:
        _type_ -- 无意义,只是为了中断
    """
    replyMsg = OlivaDiceCore.msgReply.replyMsg  
    isMatchWordStart = OlivaDiceCore.msgReply.isMatchWordStart
    getMatchWordStartRight = OlivaDiceCore.msgReply.getMatchWordStartRight
    skipSpaceStart = OlivaDiceCore.msgReply.skipSpaceStart
    skipToRight = OlivaDiceCore.msgReply.skipToRight

    tmp_at_str = OlivOS.messageAPI.PARA.at(plugin_event.base_info['self_id']).CQ()
    tmp_id_str = str(plugin_event.base_info['self_id'])
    tmp_at_str_sub = None
    tmp_id_str_sub = None
    if 'sub_self_id' in plugin_event.data.extend:
        if plugin_event.data.extend['sub_self_id'] != None:
            tmp_at_str_sub = OlivOS.messageAPI.PARA.at(plugin_event.data.extend['sub_self_id']).CQ()
            tmp_id_str_sub = str(plugin_event.data.extend['sub_self_id'])
    tmp_command_str_1 = '.'
    tmp_command_str_2 = '。'
    tmp_command_str_3 = '/'
    tmp_reast_str = plugin_event.data.message
    flag_force_reply = False
    flag_is_command = False
    flag_is_from_host = False
    flag_is_from_group = False
    flag_is_from_group_admin = False
    flag_is_from_group_have_admin = False
    flag_is_from_master = False
    if isMatchWordStart(tmp_reast_str, '[CQ:reply,id='):
        tmp_reast_str = skipToRight(tmp_reast_str, ']')
        tmp_reast_str = tmp_reast_str[1:]
    if flag_force_reply is False:
        tmp_reast_str_old = tmp_reast_str
        tmp_reast_obj = OlivOS.messageAPI.Message_templet(
            'old_string',
            tmp_reast_str
        )
        tmp_at_list = []
        for tmp_reast_obj_this in tmp_reast_obj.data:
            tmp_para_str_this = tmp_reast_obj_this.CQ()
            if type(tmp_reast_obj_this) is OlivOS.messageAPI.PARA.at:
                tmp_at_list.append(str(tmp_reast_obj_this.data['id']))
                tmp_reast_str = tmp_reast_str.lstrip(tmp_para_str_this)
            elif type(tmp_reast_obj_this) is OlivOS.messageAPI.PARA.text:
                if tmp_para_str_this.strip(' ') == '':
                    tmp_reast_str = tmp_reast_str.lstrip(tmp_para_str_this)
                else:
                    break
            else:
                break
        if tmp_id_str in tmp_at_list:
            flag_force_reply = True
        if tmp_id_str_sub in tmp_at_list:
            flag_force_reply = True
        if 'all' in tmp_at_list:
            flag_force_reply = True
        if flag_force_reply is True:
            tmp_reast_str = skipSpaceStart(tmp_reast_str)
        else:
            tmp_reast_str = tmp_reast_str_old
    if flag_is_command:
        tmp_hagID = None
        if plugin_event.plugin_info['func_type'] == 'group_message':
            if plugin_event.data.host_id != None:
                flag_is_from_host = True
            flag_is_from_group = True
        elif plugin_event.plugin_info['func_type'] == 'private_message':
            flag_is_from_group = False
        if flag_is_from_group:
            if 'role' in plugin_event.data.sender:
                flag_is_from_group_have_admin = True
                if plugin_event.data.sender['role'] in ['owner', 'admin']:
                    flag_is_from_group_admin = True
                elif plugin_event.data.sender['role'] in ['sub_admin']:
                    flag_is_from_group_admin = True
                    flag_is_from_group_sub_admin = True
        if flag_is_from_host and flag_is_from_group:
            tmp_hagID = '%s|%s' % (str(plugin_event.data.host_id), str(plugin_event.data.group_id))
        elif flag_is_from_group:
            tmp_hagID = str(plugin_event.data.group_id)
        flag_hostEnable = True
        if flag_is_from_host:
            flag_hostEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = plugin_event.data.host_id,
                userType = 'host',
                platform = plugin_event.platform['platform'],
                userConfigKey = 'hostEnable',
                botHash = plugin_event.bot_info.hash
            )
        flag_hostLocalEnable = True
        if flag_is_from_host:
            flag_hostLocalEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                userId = plugin_event.data.host_id,
                userType = 'host',
                platform = plugin_event.platform['platform'],
                userConfigKey = 'hostLocalEnable',
                botHash = plugin_event.bot_info.hash
            )
        flag_groupEnable = True
        if flag_is_from_group:
            if flag_is_from_host:
                if flag_hostEnable:
                    flag_groupEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                        userId = tmp_hagID,
                        userType = 'group',
                        platform = plugin_event.platform['platform'],
                        userConfigKey = 'groupEnable',
                        botHash = plugin_event.bot_info.hash
                    )
                else:
                    flag_groupEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                        userId = tmp_hagID,
                        userType = 'group',
                        platform = plugin_event.platform['platform'],
                        userConfigKey = 'groupWithHostEnable',
                        botHash = plugin_event.bot_info.hash
                    )
            else:
                flag_groupEnable = OlivaDiceCore.userConfig.getUserConfigByKey(
                    userId = tmp_hagID,
                    userType = 'group',
                    platform = plugin_event.platform['platform'],
                    userConfigKey = 'groupEnable',
                    botHash = plugin_event.bot_info.hash
                )
        #此频道关闭时中断处理
        if not flag_hostLocalEnable and not flag_force_reply:
            return
        #此群关闭时中断处理
        if not flag_groupEnable and not flag_force_reply:
            return
    petpetqq = checkpetpet(settings.recheck, tmp_reast_str)
    res = ""
    if petpetqq:
        res: str = petpet(petpetqq)
    if res:
        plugin_event.reply(res)