"""
工具函数模块
"""
import os
import json
import pandas as pd
from datetime import datetime


def ensure_dir(directory):
    """确保目录存在"""
    if not os.path.exists(directory):
        os.makedirs(directory)


def save_json(data, filepath):
    """保存JSON文件"""
    ensure_dir(os.path.dirname(filepath))
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(filepath):
    """加载JSON文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_csv(data, filepath):
    """保存CSV文件"""
    ensure_dir(os.path.dirname(filepath))
    if isinstance(data, pd.DataFrame):
        data.to_csv(filepath, index=False, encoding='utf-8-sig')
    else:
        pd.DataFrame(data).to_csv(filepath, index=False, encoding='utf-8-sig')


def load_csv(filepath):
    """加载CSV文件"""
    return pd.read_csv(filepath, encoding='utf-8-sig')


def get_timestamp():
    """获取当前时间戳字符串"""
    return datetime.now().strftime('%Y%m%d_%H%M%S')


def print_progress(current, total, prefix='Progress'):
    """打印进度条"""
    percent = current / total * 100
    bar_length = 50
    filled = int(bar_length * current / total)
    bar = '█' * filled + '-' * (bar_length - filled)
    print(f'\r{prefix}: |{bar}| {percent:.1f}% ({current}/{total})', end='')
    if current >= total:
        print()
