import OlivOS
import echo

class Event(object):
    def init(plugin_event, Proc):
        pass
        
    def private_message(plugin_event, Proc):
        unity_reply(plugin_event, Proc)

    def group_message(plugin_event, Proc):
        unity_reply(plugin_event, Proc)


def unity_reply(plugin_event, Proc):
    msg = plugin_event.data.message
    if msg.startswith('.echo') or msg.startswith('。echo'):
        echo_content = msg[5:].strip()
        if echo_content:  # 如果有内容
            plugin_event.reply(echo_content)
        else:
            plugin_event.reply('请输入要小芙重复的的内容哦！例如: .echo 你好')