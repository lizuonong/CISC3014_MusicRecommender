"""
配置文件
"""
import os

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# 数据目录
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')

# 输出目录
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')

# 爬虫配置
CRAWLER_CONFIG = {
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'download_delay': 1.5,
    'concurrent_requests': 4,
    'max_pages': 5,  # 最大爬取页数
    'songs_per_playlist': 20,  # 每个歌单最多爬取歌曲数
}

# 推荐系统配置
RECOMMENDER_CONFIG = {
    'method': 'user',  # 'user' 或 'item'
    'top_k': 5,  # 使用最相似的k个用户/物品
    'top_n': 10,  # 推荐数量
}

# 数据处理配置
PROCESSOR_CONFIG = {
    'play_count_weight': 0.6,  # 播放量权重
    'comment_count_weight': 0.4,  # 评论数权重
    'min_rating': 0.1,  # 最小评分阈值
}

# 确保目录存在
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, OUTPUT_DIR]:
    os.makedirs(directory, exist_ok=True)
