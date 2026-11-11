"""
快速开始脚本 - 使用模拟数据测试推荐系统
"""
import os
import sys
import pandas as pd

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generate_mock_data import save_mock_data
from src.analysis.data_processor import DataProcessor
from src.analysis.recommender import CollaborativeFiltering
from src.utils.helpers import save_csv


def quick_start():
    """快速开始"""
    print('=' * 60)
    print('🎵 音乐推荐系统 - 快速开始')
    print('=' * 60)
    
    # 1. 生成模拟数据
    print('\n📊 步骤 1/4: 生成模拟数据...')
    songs_df, ratings_df, playlists_df = save_mock_data()
    
    # 2. 处理数据
    print('\n🔧 步骤 2/4: 处理数据...')
    processor = DataProcessor()
    
    # 合并歌曲和歌单数据
    merged_df = playlists_df.merge(songs_df[['song_id', 'title', 'artist']], on='song_id', how='left')
    
    # 处理数据
    processed_df = processor.clean_data(merged_df)
    processed_df = processor.extract_tags(processed_df)
    
    # 3. 训练模型
    print('\n🤖 步骤 3/4: 训练推荐模型...')
    user_item_matrix = processor.create_user_item_matrix(processed_df)
    
    # 转换为训练数据
    train_data = []
    for user in user_item_matrix.index:
        for item in user_item_matrix.columns:
            rating = user_item_matrix.loc[user, item]
            if rating > 0:
                train_data.append({
                    'user_id': user,
                    'item_id': item,
                    'rating': rating
                })
    
    train_df = pd.DataFrame(train_data)
    
    # 训练模型
    model = CollaborativeFiltering(method='user')
    model.fit(train_df)
    
    print(f'✓ 用户-物品矩阵形状: {user_item_matrix.shape}')
    print(f'✓ 训练数据量: {len(train_df)} 条')
    
    # 4. 生成推荐
    print('\n🎯 步骤 4/4: 生成推荐...')
    recommendations = {}
    
    for user in list(user_item_matrix.index)[:5]:  # 为前5个用户生成推荐
        user_recs = model.recommend(user, top_n=5)
        recommendations[user] = user_recs
    
    # 显示推荐结果
    print('\n' + '=' * 60)
    print('📋 推荐结果示例')
    print('=' * 60)
    
    for user, recs in recommendations.items():
        print(f'\n👤 用户: {user}')
        for i, (song_id, score) in enumerate(recs, 1):
            print(f'   {i}. {song_id} (预测评分: {score:.4f})')
    
    # 保存结果
    os.makedirs('output', exist_ok=True)
    rec_data = []
    for user, recs in recommendations.items():
        for song_id, score in recs:
            rec_data.append({
                'user_id': user,
                'song_id': song_id,
                'predicted_rating': score
            })
    
    rec_df = pd.DataFrame(rec_data)
    rec_df.to_csv('output/quick_start_recommendations.csv', index=False, encoding='utf-8-sig')
    
    print('\n' + '=' * 60)
    print('✅ 快速开始完成！')
    print('=' * 60)
    print(f'\n📁 生成的文件:')
    print(f'   - data/raw/songs.csv')
    print(f'   - data/raw/ratings.csv')
    print(f'   - data/raw/playlists.csv')
    print(f'   - output/quick_start_recommendations.csv')
    print('\n💡 提示:')
    print('   - 运行 python main.py --crawl 爬取真实数据')
    print('   - 运行 python main.py --all 执行完整流程')
    print('   - 打开 notebooks/analysis.ipynb 查看可视化分析')


if __name__ == '__main__':
    quick_start()
