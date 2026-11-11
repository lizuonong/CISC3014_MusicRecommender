"""
数据处理模块 - 清洗和预处理爬取的音乐数据
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import re


class DataProcessor:
    """数据处理器"""
    
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.processed_data = None
    
    def load_data(self, filepath):
        """加载数据"""
        df = pd.read_csv(filepath)
        print(f'加载数据: {len(df)} 条记录')
        return df
    
    def clean_data(self, df):
        """清洗数据"""
        # 删除空值
        df = df.dropna(subset=['title', 'artist'])
        
        # 删除重复数据
        df = df.drop_duplicates(subset=['song_id'])
        
        # 清理字符串字段
        df['title'] = df['title'].astype(str).str.strip()
        df['artist'] = df['artist'].astype(str).str.strip()
        
        # 处理数值字段
        df['play_count'] = pd.to_numeric(df['play_count'], errors='coerce').fillna(0)
        df['comment_count'] = pd.to_numeric(df['comment_count'], errors='coerce').fillna(0)
        
        print(f'清洗后数据: {len(df)} 条记录')
        return df
    
    def extract_tags(self, df):
        """提取和清理标签"""
        def clean_tags(tags_str):
            if pd.isna(tags_str) or tags_str == '':
                return []
            tags = str(tags_str).split(',')
            return [tag.strip() for tag in tags if tag.strip()]
        
        df['tags_list'] = df['tags'].apply(clean_tags)
        df['tags_combined'] = df['tags_list'].apply(lambda x: ' '.join(x))
        
        return df
    
    def normalize_features(self, df):
        """归一化数值特征"""
        features = ['play_count', 'comment_count']
        df[features] = self.scaler.fit_transform(df[features])
        return df
    
    def create_user_item_matrix(self, df, threshold=0.5):
        """
        创建用户-物品评分矩阵
        
        基于播放量和评论数生成评分
        """
        # 计算综合评分
        df['rating'] = (df['play_count'] * 0.6 + df['comment_count'] * 0.4)
        
        # 创建用户-物品矩阵（这里简化为歌单-歌曲矩阵）
        user_item_matrix = df.pivot_table(
            index='playlist_name',
            columns='song_id',
            values='rating',
            aggfunc='mean'
        ).fillna(0)
        
        return user_item_matrix
    
    def process(self, filepath):
        """完整的数据处理流程"""
        # 加载数据
        df = self.load_data(filepath)
        
        # 清洗数据
        df = self.clean_data(df)
        
        # 提取标签
        df = self.extract_tags(df)
        
        # 归一化特征
        df = self.normalize_features(df)
        
        self.processed_data = df
        
        print('数据处理完成！')
        return df


class FeatureExtractor:
    """特征提取器"""
    
    @staticmethod
    def extract_audio_features(song_data):
        """提取音频特征（模拟）"""
        # 实际项目中可以从音频文件提取特征
        # 这里使用歌曲的元数据作为特征
        features = {
            'play_count': song_data.get('play_count', 0),
            'comment_count': song_data.get('comment_count', 0),
            'popularity': song_data.get('play_count', 0) * 0.7 + song_data.get('comment_count', 0) * 0.3
        }
        return features
    
    @staticmethod
    def compute_similarity(song1, song2, method='cosine'):
        """计算歌曲相似度"""
        from sklearn.metrics.pairwise import cosine_similarity
        
        # 基于标签的相似度
        tags1 = set(song1.get('tags_list', []))
        tags2 = set(song2.get('tags_list', []))
        
        if not tags1 or not tags2:
            return 0
        
        # Jaccard相似度
        intersection = len(tags1 & tags2)
        union = len(tags1 | tags2)
        
        return intersection / union if union > 0 else 0
