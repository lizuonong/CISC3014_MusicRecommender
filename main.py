"""
主程序 - 运行爬虫和推荐系统
"""
import os
import sys
import argparse
from datetime import datetime

# 添加项目根目录到路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.crawler.netease_spider import NetEaseMusicSpider
from src.analysis.data_processor import DataProcessor
from src.analysis.recommender import CollaborativeFiltering
from src.utils.helpers import save_csv, load_csv, ensure_dir


def run_crawler():
    """运行爬虫"""
    print('=' * 50)
    print('开始爬取网易云音乐数据...')
    print('=' * 50)
    
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings
    
    # 确保输出目录存在
    ensure_dir('data/raw')
    
    # 配置爬虫
    output_file = f'data/raw/music_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'FEED_URI': f'file:///{os.path.abspath(output_file)}',
        'FEED_FORMAT': 'csv',
        'DOWNLOAD_DELAY': 1.5,
        'CONCURRENT_REQUESTS': 4,
        'ROBOTSTXT_OBEY': False,
        'LOG_LEVEL': 'INFO'
    })
    
    process.crawl(NetEaseMusicSpider)
    process.start()
    
    print(f'\n爬虫完成！数据已保存到: {output_file}')
    return output_file


def process_data(input_file):
    """处理数据"""
    print('\n' + '=' * 50)
    print('开始处理数据...')
    print('=' * 50)
    
    processor = DataProcessor()
    df = processor.process(input_file)
    
    # 保存处理后的数据
    ensure_dir('data/processed')
    output_file = 'data/processed/music_data_clean.csv'
    save_csv(df, output_file)
    
    print(f'处理后的数据已保存到: {output_file}')
    return output_file, df


def train_model(df):
    """训练推荐模型"""
    print('\n' + '=' * 50)
    print('开始训练推荐模型...')
    print('=' * 50)
    
    # 创建用户-物品矩阵
    processor = DataProcessor()
    user_item_matrix = processor.create_user_item_matrix(df)
    
    print(f'用户-物品矩阵形状: {user_item_matrix.shape}')
    
    # 转换为训练数据格式
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
    
    print('模型训练完成！')
    return model, user_item_matrix


def generate_recommendations(model, user_item_matrix, n_recommendations=10):
    """生成推荐"""
    print('\n' + '=' * 50)
    print('开始生成推荐...')
    print('=' * 50)
    
    recommendations = {}
    
    for user in user_item_matrix.index[:10]:  # 为前10个用户生成推荐
        user_recs = model.recommend(user, top_n=n_recommendations)
        recommendations[user] = user_recs
        print(f'为用户 {user} 生成了 {len(user_recs)} 条推荐')
    
    # 保存推荐结果
    ensure_dir('output')
    rec_data = []
    for user, recs in recommendations.items():
        for song_id, score in recs:
            rec_data.append({
                'user_id': user,
                'song_id': song_id,
                'predicted_rating': score
            })
    
    rec_df = pd.DataFrame(rec_data)
    save_csv(rec_df, 'output/recommendations.csv')
    
    print(f'推荐结果已保存到: output/recommendations.csv')
    return recommendations


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='音乐推荐系统')
    parser.add_argument('--crawl', action='store_true', help='运行爬虫')
    parser.add_argument('--process', action='store_true', help='处理数据')
    parser.add_argument('--train', action='store_true', help='训练模型')
    parser.add_argument('--recommend', action='store_true', help='生成推荐')
    parser.add_argument('--all', action='store_true', help='运行完整流程')
    parser.add_argument('--input', type=str, help='输入数据文件路径')
    
    args = parser.parse_args()
    
    # 如果没有指定任何参数，显示帮助信息
    if not any([args.crawl, args.process, args.train, args.recommend, args.all]):
        parser.print_help()
        return
    
    input_file = args.input
    
    # 运行完整流程
    if args.all or args.crawl:
        input_file = run_crawler()
    
    if args.all or args.process:
        if not input_file:
            # 使用最新的数据文件
            import glob
            files = glob.glob('data/raw/music_data_*.csv')
            if files:
                input_file = max(files, key=os.path.getctime)
            else:
                print('错误: 未找到数据文件，请先运行爬虫')
                return
        
        output_file, df = process_data(input_file)
    
    if args.all or args.train:
        if 'df' not in locals():
            # 加载处理后的数据
            df = load_csv('data/processed/music_data_clean.csv')
        
        model, user_item_matrix = train_model(df)
    
    if args.all or args.recommend:
        if 'model' not in locals():
            print('错误: 请先训练模型')
            return
        
        recommendations = generate_recommendations(model, user_item_matrix)
    
    print('\n' + '=' * 50)
    print('流程完成！')
    print('=' * 50)


if __name__ == '__main__':
    import pandas as pd
    main()
