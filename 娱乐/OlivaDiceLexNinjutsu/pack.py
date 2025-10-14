# -*- coding: utf-8 -*-
"""
OlivaDice 忍术释放模块打包脚本
"""

import zipfile
import os

plugin_name = "OlivaDiceLexNinjutsu"
opk_file = f"{plugin_name}.opk"

# 需要排除的文件和文件夹
exclude_items = {
    "pack.py",           # 打包脚本本身
    opk_file,            # 生成的 opk 文件
    "__pycache__",       # Python 缓存目录
    ".git",              # Git 目录
    ".gitignore",        # Git 忽略文件
    ".vscode",           # VSCode 配置目录
    ".idea",             # PyCharm 配置目录
    ".md",               # Markdown 文档
}

def should_exclude(path):
    """判断文件或目录是否应该被排除"""
    name = os.path.basename(path)
    # 排除指定的文件和目录
    if name in exclude_items:
        return True
    # 排除所有 .opk 文件
    if name.endswith('.opk'):
        return True
    return False

def main():
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 删除旧文件
    if os.path.exists(opk_file):
        os.remove(opk_file)
        print(f"已删除旧文件: {opk_file}")
    
    # 获取所有需要打包的文件
    files_to_pack = []
    for root, dirs, files in os.walk('.'):
        # 过滤掉需要排除的目录
        dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]
        
        for file in files:
            file_path = os.path.join(root, file)
            # 转换为相对路径
            rel_path = os.path.relpath(file_path, '.')
            
            # 跳过需要排除的文件
            if not should_exclude(file_path):
                files_to_pack.append(rel_path)
    
    # 创建 OPK 文件（实际上是 ZIP）
    with zipfile.ZipFile(opk_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in sorted(files_to_pack):
            if os.path.exists(file):
                zf.write(file)
                print(f"✓ 已添加: {file}")
            else:
                print(f"✗ 文件不存在: {file}")
    
    # 检查文件大小
    file_size = os.path.getsize(opk_file)
    file_size_kb = file_size / 1024
    
    print(f"\n{'='*50}")
    print(f"打包完成: {opk_file}")
    print(f"文件数量: {len(files_to_pack)}")
    print(f"文件大小: {file_size_kb:.2f} KB")
    print(f"{'='*50}")
    print("\n安装方法：")
    print("1. 将 OPK 文件复制到 OlivaDice 插件目录")
    print("2. 重启 OlivaDice 或重新加载插件")

if __name__ == "__main__":
    main()
