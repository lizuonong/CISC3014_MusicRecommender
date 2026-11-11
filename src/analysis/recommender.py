"""
推荐算法模块 - 实现协同过滤推荐
"""
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler


class CollaborativeFiltering:
    """协同过滤推荐算法"""
    
    def __init__(self, method='user'):
        """
        初始化推荐器
        
        Args:
            method: 'user' 基于用户 或 'item' 基于物品
        """
        self.method = method
        self.user_item_matrix = None
        self.similarity_matrix = None
        self.scaler = MinMaxScaler()
    
    def fit(self, data):
        """
        训练模型
        
        Args:
            data: DataFrame，包含 user_id, item_id, rating 列
        """
        # 构建用户-物品评分矩阵
        self.user_item_matrix = data.pivot_table(
            index='user_id', 
            columns='item_id', 
            values='rating'
        ).fillna(0)
        
        # 计算相似度矩阵
        if self.method == 'user':
            self.similarity_matrix = cosine_similarity(self.user_item_matrix)
        else:
            self.similarity_matrix = cosine_similarity(self.user_item_matrix.T)
        
        return self
    
    def predict(self, user_id, item_id, top_k=5):
        """
        预测用户对物品的评分
        
        Args:
            user_id: 用户ID
            item_id: 物品ID
            top_k: 使用最相似的k个用户/物品
            
        Returns:
            float: 预测评分
        """
        if self.similarity_matrix is None:
            raise ValueError("模型未训练，请先调用 fit() 方法")
        
        # 获取相似度
        if self.method == 'user':
            user_idx = list(self.user_item_matrix.index).index(user_id)
            similarities = self.similarity_matrix[user_idx]
            ratings = self.user_item_matrix[item_id].values
        else:
            item_idx = list(self.user_item_matrix.columns).index(item_id)
            similarities = self.similarity_matrix[item_idx]
            ratings = self.user_item_matrix.loc[user_id].values
        
        # 选择最相似的top_k个
        top_indices = np.argsort(similarities)[-top_k:]
        top_similarities = similarities[top_indices]
        top_ratings = ratings[top_indices]
        
        # 加权平均
        if top_similarities.sum() == 0:
            return 0
        prediction = np.average(top_ratings, weights=top_similarities)
        
        return prediction
    
    def recommend(self, user_id, top_n=10):
        """
        为用户推荐物品
        
        Args:
            user_id: 用户ID
            top_n: 推荐数量
            
        Returns:
            list: 推荐的物品ID列表
        """
        if self.user_item_matrix is None:
            raise ValueError("模型未训练")
        
        # 获取用户未评分的物品
        user_ratings = self.user_item_matrix.loc[user_id]
        unrated_items = user_ratings[user_ratings == 0].index
        
        # 预测评分
        predictions = []
        for item_id in unrated_items:
            pred = self.predict(user_id, item_id)
            predictions.append((item_id, pred))
        
        # 按预测评分排序
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        return predictions[:top_n]


class TFIDFRecommender:
    """基于TF-IDF的推荐算法（用于标签相似度）"""
    
    def __init__(self):
        self.tfidf_matrix = None
        self.item_indices = None
    
    def fit(self, tags_data):
        """
        训练TF-IDF模型
        
        Args:
            tags_data: DataFrame，包含 item_id, tags 列
        """
        from sklearn.feature_extraction.text import TfidfVectorizer
        
        vectorizer = TfidfVectorizer()
        self.tfidf_matrix = vectorizer.fit_transform(tags_data['tags'])
        self.item_indices = tags_data['item_id'].values
        
        return self
    
    def recommend(self, item_id, top_n=10):
        """
        基于标签相似度推荐
        
        Args:
            item_id: 物品ID
            top_n: 推荐数量
            
        Returns:
            list: 相似物品列表
        """
        if self.tfidf_matrix is None:
            raise ValueError("模型未训练")
        
        item_idx = list(self.item_indices).index(item_id)
        similarities = cosine_similarity(self.tfidf_matrix[item_idx], self.tfidf_matrix).flatten()
        
        # 获取最相似的物品
        top_indices = np.argsort(similarities)[-top_n-1:-1][::-1]
        
        return [(self.item_indices[i], similarities[i]) for i in top_indices]
