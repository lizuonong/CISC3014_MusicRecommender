"""
音乐数据爬虫 - 从音乐网站爬取歌曲信息
"""
import scrapy
import json
from datetime import datetime


class MusicSpider(scrapy.Spider):
    """音乐爬虫基类"""
    name = 'music_spider'
    
    # 配置项 - 根据实际情况修改
    start_urls = []  # 起始URL列表
    allowed_domains = []  # 允许的域名
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'DOWNLOAD_DELAY': 1,  # 下载延迟，避免被封
        'CONCURRENT_REQUESTS': 4,
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.crawl_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.items_collected = 0
    
    def parse(self, response):
        """解析页面 - 子类需要实现"""
        raise NotImplementedError("子类需要实现 parse 方法")
    
    def save_item(self, item):
        """保存单个数据项"""
        self.items_collected += 1
        self.logger.info(f"已收集 {self.items_collected} 条数据")
        return item
    
    def closed(self, reason):
        """爬虫关闭时的回调"""
        self.logger.info(f"爬虫关闭，原因: {reason}")
        self.logger.info(f"总共收集 {self.items_collected} 条数据")
