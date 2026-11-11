"""
网易云音乐爬虫 - 爬取歌单和歌曲数据
"""
import scrapy
import json
import time
from datetime import datetime
from urllib.parse import urlencode


class NetEaseMusicSpider(scrapy.Spider):
    """网易云音乐爬虫"""
    name = 'netease_music'
    allowed_domains = ['music.163.com']
    
    # 配置
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'DOWNLOAD_DELAY': 1.5,
        'CONCURRENT_REQUESTS': 4,
        'ROBOTSTXT_OBEY': False,
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.crawl_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.songs_collected = 0
        self.playlists_collected = 0
        
    def start_requests(self):
        """生成起始请求"""
        # 爬取热门歌单
        for page in range(1, 6):  # 爬取前5页
            url = f'https://music.163.com/discover/playlist/?order=hot&cat=全部&limit=35&offset={(page-1)*35}'
            yield scrapy.Request(url, callback=self.parse_playlist)
    
    def parse_playlist(self, response):
        """解析歌单列表"""
        # 提取歌单链接
        playlist_links = response.css('ul.m-cvylst li a.msk::attr(href)').getall()
        
        for link in playlist_links:
            playlist_id = link.split('=')[-1]
            detail_url = f'https://music.163.com/playlist?id={playlist_id}'
            yield scrapy.Request(detail_url, callback=self.parse_playlist_detail)
    
    def parse_playlist_detail(self, response):
        """解析歌单详情"""
        self.playlists_collected += 1
        
        # 提取歌单信息
        playlist_name = response.css('h2.f-ff2.f-brk::text').get('')
        
        # 提取歌曲列表
        song_links = response.css('ul.m-cvylst li a.msk::attr(href)').getall()
        
        # 如果没有找到歌曲，尝试其他选择器
        if not song_links:
            song_links = response.css('table tbody tr[data-id]::attr(data-id)').getall()
        
        for song_id in song_links[:20]:  # 每个歌单最多爬20首歌
            if song_id.isdigit():
                song_url = f'https://music.163.com/song?id={song_id}'
                yield scrapy.Request(
                    song_url,
                    callback=self.parse_song,
                    meta={'playlist_name': playlist_name}
                )
    
    def parse_song(self, response):
        """解析歌曲详情"""
        self.songs_collected += 1
        
        # 提取歌曲信息
        title = response.css('h1.f-ff2.f-brk::text').get('')
        artist = response.css('p.des.s-fc4 a.s-fc7::text').get('')
        album = response.css('a.s-fc7::text').get('')
        
        # 提取播放量、评论数等
        play_count = response.css('span.s-fc6::text').re_first(r'(\d+)')
        comment_count = response.css('span.s-fc6::text').re_first(r'共(\d+)条评论')
        
        # 提取标签
        tags = response.css('div.tag-area a::text').getall()
        
        item = {
            'song_id': response.url.split('=')[-1],
            'title': title.strip() if title else '',
            'artist': artist.strip() if artist else '',
            'album': album.strip() if album else '',
            'play_count': int(play_count) if play_count else 0,
            'comment_count': int(comment_count) if comment_count else 0,
            'tags': ','.join(tags),
            'playlist_name': response.meta.get('playlist_name', ''),
            'crawl_time': self.crawl_time
        }
        
        if self.songs_collected % 10 == 0:
            self.logger.info(f'已爬取 {self.songs_collected} 首歌曲')
        
        yield item
    
    def closed(self, reason):
        """爬虫关闭时的回调"""
        self.logger.info(f'爬虫关闭，原因: {reason}')
        self.logger.info(f'总共爬取 {self.playlists_collected} 个歌单')
        self.logger.info(f'总共爬取 {self.songs_collected} 首歌曲')


class NetEaseAPI:
    """网易云音乐API接口（备用方案）"""
    
    BASE_URL = 'https://music.163.com/api'
    
    @staticmethod
    def get_playlist(playlist_id):
        """获取歌单详情"""
        url = f'{NetEaseAPI.BASE_URL}/v3/playlist/detail'
        params = {'id': playlist_id}
        # 这里需要添加请求逻辑
        return url, params
    
    @staticmethod
    def get_song_detail(song_id):
        """获取歌曲详情"""
        url = f'{NetEaseAPI.BASE_URL}/v3/song/detail'
        params = {'ids': song_id}
        return url, params
    
    @staticmethod
    def get_comments(song_id, page=1, limit=20):
        """获取歌曲评论"""
        url = f'{NetEaseAPI.BASE_URL}/v1/resource/comments'
        params = {'id': song_id, 'limit': limit, 'offset': (page-1)*limit}
        return url, params
