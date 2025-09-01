"""主入口
"""
import OlivOS

from . import plugin_functions


class Event(object):
    @staticmethod
    def init(plugin_event, Proc):
        """这里需要做的事情：
            初始化文件夹
            初始化配置文件
            初始化账号表
            读取文件配置
        """
        plugin_functions.basic_init()

    def private_message(plugin_event, Proc):
        """私聊事件

        Arguments:
            plugin_event {_type_} -- _description_
            Proc {_type_} -- _description_
        """
        pass

    def group_message(plugin_event, Proc):
        """群聊事件

        Arguments:
            plugin_event {_type_} -- _description_
            Proc {_type_} -- _description_
        """
        print("me go")
        plugin_functions.pg_main(plugin_event)

    @staticmethod
    def poke(plugin_event, Proc):
        """戳一戳事件

        Arguments:
            plugin_event {_type_} -- _description_
            Proc {_type_} -- _description_
        """
        pass

    @staticmethod
    def save(plugin_event, Proc):
        """保存事件

        Arguments:
            plugin_event {_type_} -- _description_
            Proc {_type_} -- _description_
        """
        pass

    @staticmethod
    def menu(plugin_event, Proc):
        """菜单栏

        Arguments:
            plugin_event {_type_} -- _description_
            Proc {_type_} -- _description_
        """
        pass
