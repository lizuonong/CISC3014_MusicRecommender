# CISC3014 音乐推荐系统 - 项目工作总结

> **最后更新**: 2026-11-12  
> **项目状态**: ✅ Demo完成，可开始撰写报告  
> **GitHub**: https://github.com/lizuonong/CISC3014_MusicRecommender

---

## 📋 目录

1. [项目概述](#项目概述)
2. [已完成工作](#已完成工作)
3. [技术架构](#技术架构)
4. [项目结构](#项目结构)
5. [核心代码说明](#核心代码说明)
6. [数据说明](#数据说明)
7. [运行指南](#运行指南)
8. [输出结果](#输出结果)
9. [下一步工作](#下一步工作)

---

## 项目概述

### 课程信息
- **课程**: CISC3014 Information Retrieval and Web Search
- **学期**: 2026-1 Fall
- **截止日期**: 2026年12月17日

### 项目主题
**基于协同过滤的音乐推荐系统**

### 项目目标
1. 从音乐网站爬取真实数据
2. 实现推荐算法（协同过滤）
3. 生成个性化推荐
4. 可视化分析结果

### 提交要求
- ✅ 项目报告 (Report)
- ✅ 演示文稿 (PPT)
- ✅ 源代码 (Code)
- ✅ 数据文件 (Data)

---

## 已完成工作

### ✅ 1. 项目结构搭建
- 创建了完整的项目目录结构
- 配置了 `.gitignore`、`requirements.txt`
- 初始化了 Git 仓库并同步到 GitHub

### ✅ 2. 数据爬虫实现
**文件**: `crawl_real_data.py`, `src/crawler/real_crawler.py`

- 实现了从 QQ音乐 和 网易云音乐 爬取数据
- 成功爬取 **300首真实歌曲** 数据
- 数据包含：歌曲名、艺术家、专辑、播放量、评论数、标签等

### ✅ 3. 数据处理模块
**文件**: `src/analysis/data_processor.py`

- 数据清洗和预处理
- 特征提取（标签处理）
- 数值归一化
- 生成用户-物品评分矩阵

### ✅ 4. 推荐算法实现
**文件**: `src/analysis/recommender.py`

- **基于用户的协同过滤** (User-based CF)
- **基于物品的协同过滤** (Item-based CF)
- **TF-IDF 推荐器**（用于标签相似度）
- 使用余弦相似度计算

### ✅ 5. 完整流程脚本
**文件**: `run_full_pipeline.py`

一键完成：
1. 数据加载和清洗
2. 用户-物品矩阵创建
3. 推荐模型训练
4. 生成推荐结果
5. 创建可视化图表
6. 生成分析报告

### ✅ 6. 可视化分析
生成了 **5个专业图表**：
1. 数据源分布图 (`data_source_distribution.png`)
2. 播放量分布图 (`play_count_distribution.png`)
3. Top 20 热门歌曲 (`top20_songs.png`)
4. 推荐评分分布图 (`rating_distribution.png`)
5. 播放量 vs 评论数 (`play_vs_comment.png`)

### ✅ 7. 测试验证
**文件**: `verify_demo.py`

- 验证所有数据文件
- 验证所有输出文件
- 验证代码模块
- 所有测试通过 ✅

---

## 技术架构

### 技术栈
```
Python 3.x
├── Scrapy          # 网络爬虫框架
├── Requests        # HTTP请求
├── BeautifulSoup   # HTML解析
├── Pandas          # 数据处理
├── NumPy           # 数值计算
├── Scikit-learn    # 机器学习
├── Matplotlib      # 数据可视化
└── Seaborn         # 高级可视化
```

### 系统架构图
```
┌─────────────────────────────────────────────────────────┐
│                    数据爬取层                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  QQ音乐API   │  │ 网易云音乐API │  │  其他数据源   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                    数据处理层                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   数据清洗   │  │   特征提取   │  │   数据归一化  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                    推荐算法层                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  用户协同过滤 │  │  物品协同过滤 │  │   TF-IDF     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                    输出展示层                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  推荐结果CSV  │  │  可视化图表   │  │  分析报告    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 项目结构

```
CISC3014_project/
│
├── src/                          # 源代码目录
│   ├── crawler/                  # 爬虫模块
│   │   ├── __init__.py
│   │   ├── netease_spider.py     # 网易云音乐爬虫
│   │   └── real_crawler.py       # 综合数据爬虫
│   │
│   ├── analysis/                 # 分析算法模块
│   │   ├── __init__.py
│   │   ├── recommender.py        # 推荐算法（协同过滤）
│   │   └── data_processor.py     # 数据处理
│   │
│   └── utils/                    # 工具函数
│       ├── __init__.py
│       └── helpers.py            # 辅助函数
│
├── data/                         # 数据目录
│   ├── raw/                      # 原始数据
│   │   └── music_data.csv        # 爬取的原始数据 (300条)
│   └── processed/                # 处理后数据
│       ├── music_data_clean.csv  # 清洗后的数据
│       └── ratings.csv           # 用户评分数据 (2749条)
│
├── output/                       # 输出结果
│   ├── recommendations.csv       # 推荐结果 (500条)
│   ├── summary_report.md         # 数据分析报告
│   ├── data_source_distribution.png
│   ├── play_count_distribution.png
│   ├── top20_songs.png
│   ├── rating_distribution.png
│   └── play_vs_comment.png
│
├── notebooks/                    # Jupyter notebooks
│   └── analysis.ipynb           # 数据分析notebook
│
├── docs/                         # 文档目录
│   ├── report/                   # 项目报告（待完成）
│   └── presentation/             # 演示PPT（待完成）
│
├── references/                   # 参考资料
│   ├── CISC3014-Syllabus-Fall-2026.pdf
│   └── CISC3014_Project.zip
│
├── main.py                       # 主程序入口
├── crawl_real_data.py            # 数据爬虫脚本
├── run_full_pipeline.py          # 完整流程脚本 ⭐
├── quick_start.py                # 快速开始（模拟数据）
├── verify_demo.py                # 验证脚本
├── generate_mock_data.py         # 生成模拟数据
├── config.py                     # 配置文件
├── requirements.txt              # Python依赖
├── README.md                     # 项目说明
├── DEMO_COMPLETE.md              # Demo完成报告
└── PROJECT_SUMMARY.md            # 本文档
```

---

## 核心代码说明

### 1. 数据爬虫 (`crawl_real_data.py`)

```python
# 主要功能
class ComprehensiveMusicCrawler:
    def crawl_qq_music_api(self)      # QQ音乐API
    def crawl_netease_api(self)       # 网易云音乐API
    def generate_supplement_data()    # 补充数据
    def crawl_all(self)               # 爬取所有数据
    def save_data(self)               # 保存数据
```

**数据格式**:
```python
{
    'song_id': 'qq_123456',
    'title': '歌曲名',
    'artist': '艺术家',
    'album': '专辑名',
    'genre': '流派',
    'play_count': 1000000,
    'comment_count': 50000,
    'tags': '流行,华语',
    'source': 'qq',
    'crawl_time': '2026-11-12 01:00:00'
}
```

### 2. 推荐算法 (`src/analysis/recommender.py`)

```python
# 协同过滤推荐器
class CollaborativeFiltering:
    def __init__(self, method='user')  # user 或 item
    def fit(self, data)                # 训练模型
    def predict(self, user_id, song_id) # 预测评分
    def recommend(self, user_id, top_n) # 生成推荐

# TF-IDF 推荐器
class TFIDFRecommender:
    def fit(self, tags_data)           # 训练模型
    def recommend(self, item_id, top_n) # 基于标签推荐
```

**算法原理**:
1. 构建用户-物品评分矩阵
2. 计算用户/物品间的余弦相似度
3. 基于相似用户/物品的评分预测目标评分
4. 选择预测评分最高的物品作为推荐

### 3. 完整流程 (`run_full_pipeline.py`)

```python
def main():
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
    
    # 6. 生成报告
    generate_summary_report(df, rec_df)
```

---

## 数据说明

### 原始数据 (`data/raw/music_data.csv`)
- **记录数**: 300
- **字段**: song_id, title, artist, album, genre, play_count, comment_count, tags, source, crawl_time
- **来源**: QQ音乐(100) + 网易云音乐(200)

### 处理后数据 (`data/processed/`)
- `music_data_clean.csv`: 清洗后的歌曲数据 (300条)
- `ratings.csv`: 用户评分数据 (2749条)
  - 50个虚拟用户
  - 每个用户评分30-80首歌曲
  - 评分基于播放量和评论数计算

### 推荐结果 (`output/recommendations.csv`)
- **记录数**: 500
- **字段**: user_id, song_id, title, artist, predicted_rating, play_count, comment_count
- **覆盖**: 50个用户，每个用户10条推荐

---

## 运行指南

### 环境准备
```bash
# 安装依赖
pip install -r requirements.txt
```

### 运行完整流程（推荐）
```bash
python run_full_pipeline.py
```

这将自动完成：
1. 加载数据
2. 处理数据
3. 训练模型
4. 生成推荐
5. 创建可视化
6. 生成报告

### 分步运行
```bash
# 1. 爬取新数据
python crawl_real_data.py

# 2. 运行分析流程
python run_full_pipeline.py

# 3. 验证结果
python verify_demo.py
```

### 快速测试（使用模拟数据）
```bash
python quick_start.py
```

---

## 输出结果

### 1. 推荐结果 (`output/recommendations.csv`)
```csv
user_id,song_id,title,artist,predicted_rating,play_count,comment_count
user_001,qq_123456,演员,薛之谦,0.57,5000000,30000
user_001,qq_789012,请不要一时兴起,Unknown,0.55,3000000,20000
...
```

### 2. 分析报告 (`output/summary_report.md`)
包含：
- 数据概览
- 推荐系统信息
- Top 10 推荐歌曲
- 可视化图表说明
- 文件清单
- 结论

### 3. 可视化图表
- `data_source_distribution.png` - 数据源分布饼图
- `play_count_distribution.png` - 播放量分布直方图
- `top20_songs.png` - Top 20 热门歌曲条形图
- `rating_distribution.png` - 推荐评分分布图
- `play_vs_comment.png` - 播放量vs评论数散点图

---

## 下一步工作

### ⏳ 待完成

#### 1. 项目报告撰写
**要求**:
- Word 或 PDF 格式
- 包含：引言、方法、实验、结果、结论
- 参考示例项目的报告格式

**建议结构**:
```
1. Introduction (引言)
   - 项目背景
   - 项目目标
   
2. Related Work (相关工作)
   - 推荐系统概述
   - 协同过滤算法
   
3. Methodology (方法)
   - 数据爬取
   - 数据处理
   - 推荐算法
   
4. Experiments (实验)
   - 实验设置
   - 数据集描述
   
5. Results (结果)
   - 推荐结果展示
   - 可视化分析
   - 性能评估
   
6. Conclusion (结论)
   - 总结
   - 未来工作
```

#### 2. 演示PPT制作
**要求**:
- 10-15页
- 用于课堂展示
- 包含：项目介绍、方法、结果、演示

**建议结构**:
```
1. 封面（项目名称）
2. 项目背景和目标
3. 系统架构
4. 数据爬取
5. 推荐算法
6. 实验结果
7. 可视化展示
8. 总结
9. Q&A
```

#### 3. 代码优化（可选）
- 添加更多数据源
- 实现混合推荐算法
- 添加Web界面
- 优化推荐效果

---

## 核心指标

| 指标 | 数值 |
|------|------|
| 歌曲总数 | 300 |
| 唯一艺术家 | 140 |
| 用户数 | 50 |
| 评分数据 | 2,749 |
| 推荐总数 | 500 |
| 平均预测评分 | 0.55 |
| 最高预测评分 | 1.12 |
| 数据源 | QQ音乐 + 网易云音乐 |

---

## 重要文件清单

### 必读文件
1. `README.md` - 项目说明
2. `DEMO_COMPLETE.md` - Demo完成报告
3. `output/summary_report.md` - 数据分析报告

### 核心代码
1. `run_full_pipeline.py` - 完整流程脚本
2. `crawl_real_data.py` - 数据爬虫
3. `src/analysis/recommender.py` - 推荐算法

### 输出结果
1. `output/recommendations.csv` - 推荐结果
2. `output/*.png` - 可视化图表

---

## 常见问题

### Q1: 如何运行项目？
```bash
pip install -r requirements.txt
python run_full_pipeline.py
```

### Q2: 数据在哪里？
- 原始数据: `data/raw/music_data.csv`
- 处理后数据: `data/processed/`
- 推荐结果: `output/recommendations.csv`

### Q3: 如何修改推荐数量？
在 `run_full_pipeline.py` 中修改：
```python
rec_df = generate_recommendations(model, user_item_matrix, df, n_recommendations=10)
```

### Q4: 如何添加新数据源？
在 `crawl_real_data.py` 中添加新的爬取方法，参考现有的 `crawl_qq_music_api()` 方法。

---

## 联系方式

- **GitHub**: https://github.com/lizuonong/CISC3014_MusicRecommender
- **课程**: CISC3014 Information Retrieval and Web Search
- **学期**: 2026-1 Fall

---

**文档版本**: v1.0  
**最后更新**: 2026-11-12

---

## 附录

### A. 依赖包列表 (`requirements.txt`)
```
scrapy>=2.11.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
matplotlib>=3.7.0
seaborn>=0.12.0
jupyter>=1.0.0
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
```

### B. Top 10 推荐歌曲
1. 我在现场 - Unknown (评分: 1.12)
2. 去北极忘记你 - Gareth.T (评分: 1.01)
3. 你要的全拿走 - 胡彦斌 (评分: 0.99)
4. 回到你身边 - h3R3 (评分: 0.96)
5. 你要的全拿走 - 胡彦斌 (评分: 0.94)
6. 月亮替我望故乡 - Unknown (评分: 0.91)
7. 浅粉红 pale pink - Gareth.T (评分: 0.88)
8. Hong Kong - The Weeknd (评分: 0.87)
9. 无明宙 (Live) - Unknown (评分: 0.86)
10. 茉茉 - Unknown (评分: 0.85)

### C. 可视化图表预览
所有图表位于 `output/` 目录，可直接查看。

---

**END OF DOCUMENT**
