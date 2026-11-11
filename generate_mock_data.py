"""
生成模拟数据用于测试
"""
import pandas as pd
import numpy as np
from datetime import datetime
import os


def generate_mock_data(n_users=50, n_songs=100, n_ratings=500):
    """
    生成模拟的音乐数据
    
    Args:
        n_users: 用户数量
        n_songs: 歌曲数量
        n_ratings: 评分数量
    
    Returns:
        DataFrame: 模拟数据
    """
    np.random.seed(42)
    
    # 生成歌曲数据
    songs = []
    genres = ['流行', '摇滚', '民谣', '电子', '古典', '爵士', '嘻哈', 'R&B', '乡村', '金属']
    artists = [f'歌手{i}' for i in range(1, 31)]
    
    for i in range(n_songs):
        songs.append({
            'song_id': f'song_{i+1:04d}',
            'title': f'歌曲{i+1:04d}',
            'artist': np.random.choice(artists),
            'album': f'专辑{np.random.randint(1, 20)}',
            'genre': np.random.choice(genres),
            'play_count': np.random.randint(1000, 1000000),
            'comment_count': np.random.randint(10, 10000),
            'tags': ','.join(np.random.choice(genres, size=np.random.randint(1, 4), replace=False)),
            'duration': np.random.randint(180, 360),  # 秒
            'release_date': f'202{np.random.randint(0, 5)}-{np.random.randint(1, 13):02d}-{np.random.randint(1, 29):02d}'
        })
    
    songs_df = pd.DataFrame(songs)
    
    # 生成用户评分数据
    ratings = []
    for _ in range(n_ratings):
        user_id = f'user_{np.random.randint(1, n_users+1):03d}'
        song_id = f'song_{np.random.randint(1, n_songs+1):04d}'
        rating = np.random.randint(1, 6)  # 1-5分
        
        ratings.append({
            'user_id': user_id,
            'song_id': song_id,
            'rating': rating,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    ratings_df = pd.DataFrame(ratings)
    
    # 生成歌单数据
    playlists = []
    for i in range(10):
        playlist_songs = np.random.choice([s['song_id'] for s in songs], 
                                          size=np.random.randint(10, 30), 
                                          replace=False)
        for song_id in playlist_songs:
            playlists.append({
                'playlist_name': f'歌单{i+1}',
                'song_id': song_id,
                'play_count': np.random.randint(10000, 500000),
                'comment_count': np.random.randint(100, 5000),
                'tags': np.random.choice(genres)
            })
    
    playlists_df = pd.DataFrame(playlists)
    
    return songs_df, ratings_df, playlists_df


def save_mock_data(output_dir='data/raw'):
    """保存模拟数据"""
    os.makedirs(output_dir, exist_ok=True)
    
    print('生成模拟数据...')
    songs_df, ratings_df, playlists_df = generate_mock_data()
    
    # 保存数据
    songs_df.to_csv(f'{output_dir}/songs.csv', index=False, encoding='utf-8-sig')
    ratings_df.to_csv(f'{output_dir}/ratings.csv', index=False, encoding='utf-8-sig')
    playlists_df.to_csv(f'{output_dir}/playlists.csv', index=False, encoding='utf-8-sig')
    
    print(f'✓ 歌曲数据: {len(songs_df)} 条 -> {output_dir}/songs.csv')
    print(f'✓ 评分数据: {len(ratings_df)} 条 -> {output_dir}/ratings.csv')
    print(f'✓ 歌单数据: {len(playlists_df)} 条 -> {output_dir}/playlists.csv')
    
    return songs_df, ratings_df, playlists_df


if __name__ == '__main__':
    save_mock_data()
