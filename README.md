# CISC3014 课程项目 - 音乐推荐系统

## 项目信息
- **课程**: CISC3014 Information Retrieval and Web Search
- **学期**: 2026-1 Fall
- **截止日期**: 2026年12月17日

## 项目概述
本项目实现一个基于协同过滤的音乐推荐系统，包含：
1. **数据爬取**: 使用 Scrapy 从音乐网站爬取歌曲数据
2. **推荐算法**: 基于用户的协同过滤 (User-based CF)
3. **可视化展示**: Jupyter Notebook 展示推荐结果

## 项目结构
```
CISC3014_project/
├── docs/                    # 文档
│   ├── report/             # 项目报告
│   └── presentation/       # 演示PPT
├── src/                    # 源代码
│   ├── crawler/           # 爬虫代码
│   ├── analysis/          # 推荐算法
│   └── utils/             # 工具函数
├── data/                   # 数据
│   ├── raw/               # 原始数据
│   └── processed/         # 处理后数据
├── output/                 # 输出结果
├── notebooks/             # Jupyter notebooks
└── references/            # 参考资料
```

## 技术栈
- Python 3.x
- Scrapy (爬虫)
- Pandas (数据处理)
- Scikit-learn (机器学习)
- Matplotlib/Seaborn (可视化)
- Jupyter Notebook

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行快速测试（使用模拟数据）
```bash
python quick_start.py
```

### 3. 爬取真实数据
```bash
python main.py --crawl
```

### 4. 运行完整流程
```bash
python main.py --all
```

## 使用说明

### 命令行参数
```bash
python main.py --crawl      # 运行爬虫
python main.py --process    # 处理数据
python main.py --train      # 训练模型
python main.py --recommend  # 生成推荐
python main.py --all        # 运行完整流程
```

### 项目文件说明
- `main.py` - 主程序入口
- `quick_start.py` - 快速开始脚本
- `generate_mock_data.py` - 生成模拟数据
- `config.py` - 配置文件
- `src/crawler/` - 爬虫模块
- `src/analysis/` - 推荐算法模块
- `src/utils/` - 工具函数

## 提交内容
- [ ] 项目报告 (Report)
- [ ] 演示文稿 (PPT)
- [ ] 源代码 (Code)
- [ ] 数据文件 (Data)

## 团队成员
- 成员1: 
- 成员2: 

## 更新日志
- 2026-11-12: 初始化项目结构，实现基础爬虫和推荐算法 

