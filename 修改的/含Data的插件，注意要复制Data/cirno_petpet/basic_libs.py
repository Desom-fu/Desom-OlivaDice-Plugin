"""自己封装的工具包
创建路径
文件读写
存档操作
字典操作
"""

import os

from . import settings

class Path():
    """Path class
    Used to create folders and get file paths
    """
    @staticmethod
    def create_folder(paths: list , isbase = True):
        """Create a folder

        Keyword Arguments:
            paths {list} -- Path list
            Samples:
                [
                    [".","plugin","data"],
                    ["plugin_name"],
                    ["file_name"]
                ]
        """
        if len(paths) == 0:
            return False
        else:
            path = Path.join([paths] , isbase)
            folder = os.path.exists(path)
            if not folder:
                os.makedirs(path)
            return True

    @staticmethod
    def join(paths: list , isbase = True):
        """Join multiple paths

        Arguments:
            paths {list} -- Path list
            Samples:
                [
                    [".","plugin","data"],
                    ["plugin_name"],
                    ["file_name"]
                ]
        Returns:
            path_str -- Path string
        """
        cache_path = [""]
        if isbase:
            cache_path.extend(settings.BASE_PATH)
        list(cache_path.extend(items) for items in paths)
        cache_rev_path = os.path.join(*cache_path)
        return cache_rev_path

    @staticmethod
    def isexit(file_path):
        if os.path.exists(file_path):
            return True
        else:
            return False