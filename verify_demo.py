"""
最终验证脚本 - 检查所有组件是否正常工作
"""
import os
import sys
import pandas as pd


def verify_data_files():
    """验证数据文件"""
    print('=' * 60)
    print('📊 验证数据文件')
    print('=' * 60)
    
    required_files = [
        'data/raw/music_data.csv',
        'data/processed/music_data_clean.csv',
        'data/processed/ratings.csv'
    ]
    
    for filepath in required_files:
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            print(f'✓ {filepath}: {len(df)} 条记录')
        else:
            print(f'✗ {filepath}: 文件不存在')
            return False
    
    return True


def verify_output_files():
    """验证输出文件"""
    print('\n' + '=' * 60)
    print('📁 验证输出文件')
    print('=' * 60)
    
    required_files = [
        'output/recommendations.csv',
        'output/summary_report.md',
        'output/data_source_distribution.png',
        'output/play_count_distribution.png',
        'output/top20_songs.png',
        'output/rating_distribution.png',
        'output/play_vs_comment.png'
    ]
    
    for filepath in required_files:
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f'✓ {filepath}: {size:,} bytes')
        else:
            print(f'✗ {filepath}: 文件不存在')
            return False
    
    return True


def verify_recommendations():
    """验证推荐结果"""
    print('\n' + '=' * 60)
    print('🎯 验证推荐结果')
    print('=' * 60)
    
    rec_df = pd.read_csv('output/recommendations.csv')
    
    print(f'✓ 推荐总数: {len(rec_df)}')
    print(f'✓ 覆盖用户数: {rec_df["user_id"].nunique()}')
    print(f'✓ 平均预测评分: {rec_df["predicted_rating"].mean():.2f}')
    print(f'✓ 最高预测评分: {rec_df["predicted_rating"].max():.2f}')
    
    # 显示Top 5推荐
    print('\n📋 Top 5 推荐:')
    top5 = rec_df.nlargest(5, 'predicted_rating')
    for i, (_, rec) in enumerate(top5.iterrows(), 1):
        print(f'  {i}. {rec["title"]} - {rec["artist"]} (评分: {rec["predicted_rating"]:.2f})')
    
    return True


def verify_code_modules():
    """验证代码模块"""
    print('\n' + '=' * 60)
    print('🔧 验证代码模块')
    print('=' * 60)
    
    modules = [
        'src.crawler.netease_spider',
        'src.crawler.real_crawler',
        'src.analysis.recommender',
        'src.analysis.data_processor',
        'src.utils.helpers'
    ]
    
    for module in modules:
        try:
            __import__(module)
            print(f'✓ {module}')
        except Exception as e:
            print(f'✗ {module}: {e}')
            return False
    
    return True


def main():
    """主函数"""
    print('\n' + '=' * 60)
    print('🎵 音乐推荐系统 - 最终验证')
    print('=' * 60)
    
    checks = [
        ('数据文件', verify_data_files),
        ('输出文件', verify_output_files),
        ('推荐结果', verify_recommendations),
        ('代码模块', verify_code_modules)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f'\n✗ {name} 验证失败: {e}')
            results.append((name, False))
    
    # 总结
    print('\n' + '=' * 60)
    print('📊 验证总结')
    print('=' * 60)
    
    for name, result in results:
        status = '✓ 通过' if result else '✗ 失败'
        print(f'{status} - {name}')
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print('\n' + '=' * 60)
        print('✅ 所有验证通过！Demo已准备就绪！')
        print('=' * 60)
        print('\n📁 GitHub 仓库: https://github.com/lizuonong/CISC3014_MusicRecommender')
        print('\n📝 下一步:')
        print('   1. 查看 output/summary_report.md 了解详细分析')
        print('   2. 查看 output/recommendations.csv 了解推荐结果')
        print('   3. 查看可视化图表 (output/*.png)')
        print('   4. 开始撰写项目报告')
        return 0
    else:
        print('\n✗ 部分验证失败，请检查上述错误')
        return 1


if __name__ == '__main__':
    sys.exit(main())
