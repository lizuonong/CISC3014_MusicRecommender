# CISC3014 课程项目 - 音乐推荐系统

## 项目信息
- **课程**: CISC3014 Information Retrieval and Web Search
- **学期**: 2026-1 Fall
- **截止日期**: 2026年12月17日

## 项目概述
基于协同过滤的音乐推荐系统，包含：
1. **数据爬取**: 从QQ音乐、网易云音乐爬取歌曲数据
2. **推荐算法**: 基于用户的协同过滤 (User-based CF)
3. **可视化分析**: 生成数据分布图表和推荐结果

## 项目结构
```
CISC3014_project/
├── src/                    # 源代码
│   ├── crawler/           # 爬虫模块
│   ├── analysis/          # 推荐算法
│   └── utils/             # 工具函数
├── data/                   # 数据
│   ├── raw/               # 原始数据
│   └── processed/         # 处理后数据
├── output/                 # 输出结果（图表、报告）
├── notebooks/             # Jupyter notebooks
├── references/            # 参考资料
│
├── crawl_real_data.py     # 数据爬虫
├── run_full_pipeline.py   # 完整流程脚本
├── requirements.txt       # Python依赖
├── README.md              # 本文件
└── PROJECT_SUMMARY.md     # 详细项目文档
```

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行完整流程
```bash
python run_full_pipeline.py
```

自动完成：数据加载 → 模型训练 → 生成推荐 → 可视化图表 → 分析报告

### 3. 爬取新数据（可选）
```bash
python crawl_real_data.py
```

## 输出文件

运行后在 `output/` 目录生成：
- `recommendations.csv` - 推荐结果
- `summary_report.md` - 数据分析报告
- `*.png` - 可视化图表（5个）

## 文档

- **README.md** - 本文件，快速入门
- **PROJECT_SUMMARY.md** - 完整项目文档，包含技术细节和代码说明

## GitHub

https://github.com/lizuonong/CISC3014_MusicRecommender
