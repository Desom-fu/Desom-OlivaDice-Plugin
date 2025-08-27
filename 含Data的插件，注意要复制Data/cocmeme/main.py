import OlivOS
import os
import random

class Event(object):
    def init(plugin_event, Proc):
        pass

    def private_message(plugin_event, Proc):
        unity_reply(plugin_event, Proc)

    def group_message(plugin_event, Proc):
        unity_reply(plugin_event, Proc)

    def save(plugin_event, Proc):
        pass

def unity_reply(plugin_event, Proc):
    # 检查消息是否包含触发词
    if plugin_event.data.message.lower().strip() in ["cocmeme", "跑团梗图"]:
        # 获取 ./data/images/跑团梗图 目录中的图片文件列表
        cocmeme_dir = "./data/images/跑团梗图"
        if not os.path.exists(cocmeme_dir):
            # 如果路径不存在，返回特定消息
            plugin_event.reply ("小芙没有找到对应的路径！")
            return
        image_files = [f for f in os.listdir(cocmeme_dir) if f.lower().endswith((".png", ".jpg", ".gif"))]
        # 随机选择一张图片
        if image_files:
            selected_image = random.choice(image_files)
            image_name = os.path.basename(selected_image)
            # 构造 CQ 码发送图片
            cq_code = f"[CQ:image,file=跑团梗图/{image_name}]"
            # 使用 plugin_event.reply(message) 发送 CQ 码
            plugin_event.reply(cq_code)
        else:
            # 如果没有找到图片，发送提示消息
            plugin_event.reply("啊哦，在目录里面小芙没有找到任何的图片！")
        return
