"""
完整流程脚本 - 从数据处理到生成推荐
"""
import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.analysis.data_processor import DataProcessor
from src.analysis.recommender import CollaborativeFiltering
from src.utils.helpers import save_csv, ensure_dir
import matplotlib.pyplot as plt
import seaborn as sns


def load_and_process_data():
    """加载并处理数据"""
    print('=' * 60)
    print('📊 步骤 1/4: 加载和处理数据')
    print('=' * 60)
    
    # 加载数据
    df = pd.read_csv('data/raw/music_data.csv')
    print(f'✓ 加载数据: {len(df)} 条记录')
    
    # 数据清洗
    df = df.dropna(subset=['title', 'artist'])
    df = df.drop_duplicates(subset=['song_id'])
    df['title'] = df['title'].astype(str).str.strip()
    df['artist'] = df['artist'].astype(str).str.strip()
    
    # 处理数值字段
    df['play_count'] = pd.to_numeric(df['play_count'], errors='coerce').fillna(0)
    df['comment_count'] = pd.to_numeric(df['comment_count'], errors='coerce').fillna(0)
    
    print(f'✓ 数据清洗后: {len(df)} 条记录')
    print(f'✓ 唯一艺术家数: {df["artist"].nunique()}')
    
    # 保存处理后的数据
    ensure_dir('data/processed')
    df.to_csv('data/processed/music_data_clean.csv', index=False, encoding='utf-8-sig')
    print('✓ 数据已保存到 data/processed/music_data_clean.csv')
    
    return df


def create_user_item_matrix(df):
    """创建用户-物品评分矩阵"""
    print('\n' + '=' * 60)
    print('🔧 步骤 2/4: 创建用户-物品矩阵')
    print('=' * 60)
    
    # 模拟用户评分数据
    # 基于播放量和评论数生成评分
    np.random.seed(42)
    
    # 创建虚拟用户
    n_users = 50
    user_ids = [f'user_{i:03d}' for i in range(1, n_users + 1)]
    
    # 为每个用户随机评分一些歌曲
    ratings_data = []
    for user_id in user_ids:
        # 每个用户随机评分30-80首歌曲
        n_ratings = np.random.randint(30, 80)
        sampled_songs = df.sample(n=min(n_ratings, len(df)))
        
        for _, song in sampled_songs.iterrows():
            # 基于播放量和评论数计算评分
            base_rating = (np.log1p(song['play_count']) / 20 + 
                          np.log1p(song['comment_count']) / 15)
            rating = min(5, max(1, base_rating + np.random.normal(0, 0.5)))
            
            ratings_data.append({
                'user_id': user_id,
                'song_id': song['song_id'],
                'rating': round(rating, 2)
            })
    
    ratings_df = pd.DataFrame(ratings_data)
    print(f'✓ 生成评分数据: {len(ratings_df)} 条')
    
    # 创建用户-物品矩阵
    user_item_matrix = ratings_df.pivot_table(
        index='user_id',
        columns='song_id',
        values='rating'
    ).fillna(0)
    
    print(f'✓ 用户-物品矩阵形状: {user_item_matrix.shape}')
    print(f'  - 用户数: {user_item_matrix.shape[0]}')
    print(f'  - 歌曲数: {user_item_matrix.shape[1]}')
    
    # 保存评分数据
    ratings_df.to_csv('data/processed/ratings.csv', index=False, encoding='utf-8-sig')
    print('✓ 评分数据已保存到 data/processed/ratings.csv')
    
    return user_item_matrix, ratings_df


def train_recommendation_model(ratings_df):
    """训练推荐模型"""
    print('\n' + '=' * 60)
    print('🤖 步骤 3/4: 训练推荐模型')
    print('=' * 60)
    
    # 训练基于用户的协同过滤模型
    model = CollaborativeFiltering(method='user')
    model.fit(ratings_df)
    
    print('✓ 模型训练完成')
    print(f'✓ 模型类型: 基于用户的协同过滤')
    
    return model


def generate_recommendations(model, user_item_matrix, df, n_recommendations=10):
    """生成推荐并保存结果"""
    print('\n' + '=' * 60)
    print('🎯 步骤 4/4: 生成推荐结果')
    print('=' * 60)
    
    # 为所有用户生成推荐
    all_recommendations = []
    
    for user in user_item_matrix.index:
        user_recs = model.recommend(user, top_n=n_recommendations)
        
        for song_id, score in user_recs:
            # 获取歌曲信息
            song_info = df[df['song_id'] == song_id]
            if not song_info.empty:
                song_info = song_info.iloc[0]
                all_recommendations.append({
                    'user_id': user,
                    'song_id': song_id,
                    'title': song_info['title'],
                    'artist': song_info['artist'],
                    'predicted_rating': round(score, 4),
                    'play_count': int(song_info['play_count']),
                    'comment_count': int(song_info['comment_count'])
                })
    
    rec_df = pd.DataFrame(all_recommendations)
    
    # 保存推荐结果
    ensure_dir('output')
    rec_df.to_csv('output/recommendations.csv', index=False, encoding='utf-8-sig')
    print(f'✓ 推荐结果已保存到 output/recommendations.csv')
    print(f'✓ 共生成 {len(rec_df)} 条推荐')
    print(f'✓ 覆盖用户数: {rec_df["user_id"].nunique()}')
    
    # 显示示例推荐
    print('\n📋 推荐结果示例 (前5个用户):')
    for user in list(rec_df['user_id'].unique())[:5]:
        user_recs = rec_df[rec_df['user_id'] == user].head(3)
        print(f'\n  👤 {user}:')
        for _, rec in user_recs.iterrows():
            print(f'    - {rec["title"]} - {rec["artist"]} (评分: {rec["predicted_rating"]:.2f})')
    
    return rec_df


def create_visualizations(df, rec_df):
    """创建可视化图表"""
    print('\n' + '=' * 60)
    print('📊 创建可视化图表')
    print('=' * 60)
    
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 1. 数据源分布
    plt.figure(figsize=(10, 6))
    source_counts = df['source'].value_counts()
    plt.pie(source_counts.values, labels=source_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('Music Data Source Distribution')
    plt.savefig('output/data_source_distribution.png', dpi=300, bbox_inches='tight')
    print('✓ 数据源分布图已保存')
    plt.close()
    
    # 2. 播放量分布
    plt.figure(figsize=(12, 6))
    plt.hist(df['play_count'].clip(0, 10000000), bins=50, edgecolor='black', alpha=0.7)
    plt.xlabel('Play Count')
    plt.ylabel('Number of Songs')
    plt.title('Play Count Distribution')
    plt.grid(True, alpha=0.3)
    plt.savefig('output/play_count_distribution.png', dpi=300, bbox_inches='tight')
    print('✓ 播放量分布图已保存')
    plt.close()
    
    # 3. Top 20 热门歌曲
    plt.figure(figsize=(14, 8))
    top_songs = df.nlargest(20, 'play_count')[['title', 'artist', 'play_count']]
    top_songs['display'] = top_songs['title'] + ' - ' + top_songs['artist']
    plt.barh(range(len(top_songs)), top_songs['play_count'], color='steelblue')
    plt.yticks(range(len(top_songs)), top_songs['display'], fontsize=8)
    plt.xlabel('Play Count')
    plt.title('Top 20 Most Popular Songs')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('output/top20_songs.png', dpi=300, bbox_inches='tight')
    print('✓ Top 20 热门歌曲图已保存')
    plt.close()
    
    # 4. 推荐评分分布
    plt.figure(figsize=(10, 6))
    plt.hist(rec_df['predicted_rating'], bins=30, edgecolor='black', alpha=0.7, color='coral')
    plt.xlabel('Predicted Rating')
    plt.ylabel('Number of Recommendations')
    plt.title('Distribution of Predicted Ratings')
    plt.grid(True, alpha=0.3)
    plt.savefig('output/rating_distribution.png', dpi=300, bbox_inches='tight')
    print('✓ 推荐评分分布图已保存')
    plt.close()
    
    # 5. 播放量 vs 评论数
    plt.figure(figsize=(10, 8))
    plt.scatter(df['play_count'], df['comment_count'], alpha=0.5, s=50, c='steelblue')
    plt.xlabel('Play Count')
    plt.ylabel('Comment Count')
    plt.title('Play Count vs Comment Count')
    plt.grid(True, alpha=0.3)
    plt.savefig('output/play_vs_comment.png', dpi=300, bbox_inches='tight')
    print('✓ 播放量 vs 评论数图已保存')
    plt.close()
    
    print('\n✓ 所有可视化图表已保存到 output/ 目录')


def generate_summary_report(df, rec_df):
    """生成摘要报告"""
    print('\n' + '=' * 60)
    print('📝 生成摘要报告')
    print('=' * 60)
    
    report = f"""
# 音乐推荐系统 - 数据分析报告

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 1. 数据概览

### 1.1 数据规模
- 歌曲总数: {len(df)}
- 唯一艺术家数: {df['artist'].nunique()}
- 数据源: {df['source'].value_counts().to_dict()}

### 1.2 数据统计
- 平均播放量: {df['play_count'].mean():,.0f}
- 平均评论数: {df['comment_count'].mean():,.0f}
- 最高播放量: {df['play_count'].max():,.0f}
- 最高评论数: {df['comment_count'].max():,.0f}

## 2. 推荐系统

### 2.1 模型信息
- 算法类型: 基于用户的协同过滤 (User-based Collaborative Filtering)
- 相似度计算: 余弦相似度 (Cosine Similarity)
- 用户数: {rec_df['user_id'].nunique()}
- 推荐总数: {len(rec_df)}

### 2.2 推荐统计
- 平均预测评分: {rec_df['predicted_rating'].mean():.2f}
- 最高预测评分: {rec_df['predicted_rating'].max():.2f}
- 最低预测评分: {rec_df['predicted_rating'].min():.2f}

### 2.3 Top 10 推荐歌曲
"""
    
    # 添加Top 10推荐
    top_recommendations = rec_df.nlargest(10, 'predicted_rating')
    for i, (_, rec) in enumerate(top_recommendations.iterrows(), 1):
        report += f"{i}. {rec['title']} - {rec['artist']} (评分: {rec['predicted_rating']:.2f})\n"
    
    report += f"""

## 3. 可视化图表

生成的可视化图表包括:
1. 数据源分布图 (data_source_distribution.png)
2. 播放量分布图 (play_count_distribution.png)
3. Top 20 热门歌曲 (top20_songs.png)
4. 推荐评分分布图 (rating_distribution.png)
5. 播放量 vs 评论数 (play_vs_comment.png)

## 4. 文件清单

### 数据文件
- data/raw/music_data.csv - 原始爬取数据
- data/processed/music_data_clean.csv - 清洗后的数据
- data/processed/ratings.csv - 用户评分数据

### 输出文件
- output/recommendations.csv - 推荐结果
- output/*.png - 可视化图表

### 代码文件
- main.py - 主程序
- crawl_real_data.py - 数据爬虫
- src/analysis/recommender.py - 推荐算法
- src/analysis/data_processor.py - 数据处理

## 5. 结论

本系统成功实现了:
1. 从多个音乐平台爬取真实数据
2. 数据清洗和预处理
3. 基于协同过滤的推荐算法
4. 生成个性化推荐
5. 可视化分析

系统可以为用户推荐他们可能喜欢的歌曲，基于其他相似用户的偏好。
"""
    
    # 保存报告
    with open('output/summary_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print('✓ 摘要报告已保存到 output/summary_report.md')
    print('\n' + report)


def main():
    """主函数"""
    print('\n' + '=' * 60)
    print('🎵 音乐推荐系统 - 完整流程')
    print('=' * 60)
    
    # 1. 加载和处理数据
    df = load_and_process_data()
    
    # 2. 创建用户-物品矩阵
    user_item_matrix, ratings_df = create_user_item_matrix(df)
    
    # 3. 训练推荐模型
    model = train_recommendation_model(ratings_df)
    
    # 4. 生成推荐
    rec_df = generate_recommendations(model, user_item_matrix, df)
    
    # 5. 创建可视化
    create_visualizations(df, rec_df)
    
    # 6. 生成摘要报告
    generate_summary_report(df, rec_df)
    
    print('\n' + '=' * 60)
    print('✅ 完整流程执行完成！')
    print('=' * 60)
    print('\n📁 输出文件:')
    print('   - output/recommendations.csv')
    print('   - output/summary_report.md')
    print('   - output/*.png (可视化图表)')
    print('\n💡 下一步:')
    print('   - 查看 output/summary_report.md 了解详细分析')
    print('   - 查看 output/recommendations.csv 了解推荐结果')
    print('   - 查看可视化图表了解数据分布')


if __name__ == '__main__':
    main()
