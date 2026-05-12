# 🚀 GitTrendPulse

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/Zero_Dependencies-✓-brightgreen.svg" alt="Zero Dependencies">
  <img src="https://img.shields.io/badge/Platform-Windows%20|%20macOS%20|%20Linux-lightgrey.svg" alt="Platform">
</p>

<p align="center">
  <b>AI驱动的GitHub趋势智能分析与洞察引擎</b><br>
  <i>Zero Dependencies · Multi-dimensional Insights · Intelligent Recommendations</i>
</p>

<p align="center">
  <a href="#简体中文">简体中文</a> |
  <a href="#繁體中文">繁體中文</a> |
  <a href="#english">English</a>
</p>

---

<a name="简体中文"></a>
## 🎉 简体中文

### 项目介绍

**GitTrendPulse** 是一个轻量级、零依赖的CLI工具，专为开发者打造，提供GitHub趋势数据的**多维度智能分析**和**AI驱动洞察**。

在日常开发中，开发者常常面临以下痛点：
- 🔍 难以快速发现高质量的开源项目
- 📊 缺乏对项目健康度和成长潜力的量化评估
- 🎯 无法根据个人技术栈获取精准推荐
- 📈 无法把握技术趋势和热门方向

GitTrendPulse 通过整合GitHub API数据，结合**AI智能分析算法**，为你提供：
- ✅ 实时趋势仓库追踪
- ✅ 项目健康度评分系统
- ✅ 个性化项目推荐
- ✅ 新兴趋势预测
- ✅ 多仓库对比分析

### ✨ 核心特性

| 特性 | 描述 | 状态 |
|------|------|------|
| 🔥 **趋势追踪** | 实时获取GitHub Trending数据，支持多语言筛选 | ✅ |
| 🏥 **健康度分析** | 基于Star、Fork、活跃度等维度的综合评分系统 | ✅ |
| 🤖 **AI推荐** | 根据用户兴趣智能推荐项目 | ✅ |
| 🚀 **新兴发现** | 检测近期快速增长的新兴项目 | ✅ |
| 📊 **对比分析** | 多仓库指标对比，辅助技术选型 | ✅ |
| 📈 **增长预测** | 分析项目增长速率和发展潜力 | ✅ |
| 🎨 **精美输出** | 彩色表格、JSON、Markdown多种格式 | ✅ |
| 🌍 **零依赖** | 纯Python标准库实现，开箱即用 | ✅ |

### 🚀 快速开始

#### 环境要求

- **Python**: 3.8 或更高版本
- **操作系统**: Windows / macOS / Linux

#### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/GitTrendPulse.git
cd GitTrendPulse

# 安装（可选，支持全局命令）
pip install -e .

# 或者直接运行
python -m gittrendpulse
```

#### 基本使用

```bash
# 查看今日趋势
gittrendpulse trending

# 查看Python趋势
gittrendpulse trending --language python

# 分析仓库健康度
gittrendpulse health microsoft/vscode

# 获取AI推荐
gittrendpulse recommend --interests ai,machine-learning,python

# 发现新兴项目
gittrendpulse emerging --language javascript

# 对比多个仓库
gittrendpulse compare facebook/react vuejs/vue sveltejs/svelte

# 分析趋势模式
gittrendpulse analyze --language python

# 查看增长速率
gittrendpulse velocity torvalds/linux
```

#### 使用GitHub Token（推荐）

为了提高API限制，建议配置GitHub Token：

```bash
# 设置环境变量
export GITHUB_TOKEN="your_github_token"

# 或者在命令中指定
gittrendpulse trending --token your_github_token
```

### 📖 详细使用指南

#### 1. 趋势追踪 (trending)

```bash
# 查看本周趋势
gittrendpulse trending --since weekly

# 查看月度趋势，限制20条
gittrendpulse trending --since monthly --limit 20

# 输出JSON格式
gittrendpulse trending --output json
```

#### 2. 健康度分析 (health)

分析仓库的多维度健康指标：

```bash
gittrendpulse health facebook/react
```

输出包含：
- 💯 健康度评分 (0-100)
- ⭐ Stars / 🍴 Forks 统计
- ⚡ 活跃度评估
- 📋 Issue比例分析

#### 3. AI智能推荐 (recommend)

基于你的技术兴趣获取个性化推荐：

```bash
# 指定兴趣领域
gittrendpulse recommend --interests "machine-learning,python,data-science"

# 限制推荐数量
gittrendpulse recommend --interests ai --limit 5
```

#### 4. 新兴趋势发现 (emerging)

发现近期快速增长的新兴项目：

```bash
# 发现JavaScript新兴项目
gittrendpulse emerging --language javascript

# 设置最小Star数
gittrendpulse emerging --min-stars 100
```

#### 5. 仓库对比 (compare)

横向对比多个仓库指标：

```bash
gittrendpulse compare facebook/react vuejs/vue angular/angular
```

#### 6. 趋势模式分析 (analyze)

分析趋势仓库的语言分布和热门主题：

```bash
gittrendpulse analyze --language python
```

#### 7. 增长速率分析 (velocity)

分析项目的增长趋势和潜力预测：

```bash
gittrendpulse velocity kubernetes/kubernetes
```

### 💡 设计思路与迭代规划

#### 技术选型

- **纯Python标准库**：零第三方依赖，确保兼容性和部署便利性
- **urllib**：原生HTTP客户端，无需requests
- **argparse**：标准命令行解析
- **unittest**：标准测试框架

#### 架构设计

```
GitTrendPulse/
├── gittrendpulse/
│   ├── __init__.py          # 包初始化
│   ├── github_api.py        # GitHub API客户端
│   ├── core.py              # 核心分析引擎
│   ├── recommender.py       # AI推荐引擎
│   ├── formatter.py         # 输出格式化器
│   └── cli.py               # 命令行接口
├── tests/                   # 单元测试
├── setup.py                 # 安装配置
└── requirements.txt         # 依赖声明（空）
```

#### 迭代规划

- [x] v1.0.0 - 核心功能实现
- [ ] v1.1.0 - 添加缓存机制
- [ ] v1.2.0 - 支持导出HTML报告
- [ ] v1.3.0 - 集成更多数据源
- [ ] v2.0.0 - TUI交互界面

### 📦 打包与部署

#### 本地安装

```bash
pip install -e .
```

#### 构建分发包

```bash
python setup.py sdist bdist_wheel
```

#### 从PyPI安装（未来）

```bash
pip install gittrendpulse
```

### 🤝 贡献指南

欢迎提交Issue和PR！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源。

---

<a name="繁體中文"></a>
## 🎉 繁體中文

### 專案介紹

**GitTrendPulse** 是一個輕量級、零依賴的CLI工具，專為開發者打造，提供GitHub趨勢數據的**多維度智能分析**和**AI驅動洞察**。

在日常開發中，開發者常常面臨以下痛點：
- 🔍 難以快速發現高品質的開源專案
- 📊 缺乏對專案健康度和成長潛力的量化評估
- 🎯 無法根據個人技術棧獲取精準推薦
- 📈 無法把握技術趨勢和熱門方向

GitTrendPulse 通過整合GitHub API數據，結合**AI智能分析算法**，為你提供：
- ✅ 即時趨勢倉庫追蹤
- ✅ 專案健康度評分系統
- ✅ 個人化專案推薦
- ✅ 新興趨勢預測
- ✅ 多倉庫對比分析

### ✨ 核心特性

| 特性 | 描述 | 狀態 |
|------|------|------|
| 🔥 **趨勢追蹤** | 即時獲取GitHub Trending數據，支援多語言篩選 | ✅ |
| 🏥 **健康度分析** | 基於Star、Fork、活躍度等維度的綜合評分系統 | ✅ |
| 🤖 **AI推薦** | 根據用戶興趣智能推薦專案 | ✅ |
| 🚀 **新興發現** | 檢測近期快速增長的新興專案 | ✅ |
| 📊 **對比分析** | 多倉庫指標對比，輔助技術選型 | ✅ |
| 📈 **增長預測** | 分析專案增長速率和發展潛力 | ✅ |
| 🎨 **精美輸出** | 彩色表格、JSON、Markdown多種格式 | ✅ |
| 🌍 **零依賴** | 純Python標準庫實現，開箱即用 | ✅ |

### 🚀 快速開始

#### 環境要求

- **Python**: 3.8 或更高版本
- **作業系統**: Windows / macOS / Linux

#### 安裝

```bash
# 克隆倉庫
git clone https://github.com/gitstq/GitTrendPulse.git
cd GitTrendPulse

# 安裝（可選，支援全域命令）
pip install -e .

# 或者直接運行
python -m gittrendpulse
```

#### 基本使用

```bash
# 查看今日趨勢
gittrendpulse trending

# 查看Python趨勢
gittrendpulse trending --language python

# 分析倉庫健康度
gittrendpulse health microsoft/vscode

# 獲取AI推薦
gittrendpulse recommend --interests ai,machine-learning,python

# 發現新興專案
gittrendpulse emerging --language javascript

# 對比多個倉庫
gittrendpulse compare facebook/react vuejs/vue sveltejs/svelte

# 分析趨勢模式
gittrendpulse analyze --language python

# 查看增長速率
gittrendpulse velocity torvalds/linux
```

### 📖 詳細使用指南

請參考上方簡體中文版本的詳細文檔，所有功能和使用方法完全相同。

### 🤝 貢獻指南

歡迎提交Issue和PR！

### 📄 開源協議

本專案基於 [MIT License](LICENSE) 開源。

---

<a name="english"></a>
## 🎉 English

### Introduction

**GitTrendPulse** is a lightweight, zero-dependency CLI tool designed for developers, providing **multi-dimensional intelligent analysis** and **AI-driven insights** for GitHub trending data.

In daily development, developers often face these pain points:
- 🔍 Difficulty discovering high-quality open-source projects quickly
- 📊 Lack of quantitative assessment for project health and growth potential
- 🎯 Unable to get precise recommendations based on personal tech stack
- 📈 Cannot grasp technology trends and popular directions

GitTrendPulse integrates GitHub API data with **AI intelligent analysis algorithms** to provide:
- ✅ Real-time trending repository tracking
- ✅ Project health scoring system
- ✅ Personalized project recommendations
- ✅ Emerging trend prediction
- ✅ Multi-repository comparative analysis

### ✨ Key Features

| Feature | Description | Status |
|---------|-------------|--------|
| 🔥 **Trend Tracking** | Real-time GitHub Trending data with multi-language filtering | ✅ |
| 🏥 **Health Analysis** | Comprehensive scoring based on Stars, Forks, activity, etc. | ✅ |
| 🤖 **AI Recommendations** | Intelligent project recommendations based on user interests | ✅ |
| 🚀 **Emerging Discovery** | Detect rapidly growing emerging projects | ✅ |
| 📊 **Comparative Analysis** | Multi-repository metrics comparison for tech selection | ✅ |
| 📈 **Growth Prediction** | Analyze project growth rate and development potential | ✅ |
| 🎨 **Beautiful Output** | Colorful tables, JSON, Markdown formats | ✅ |
| 🌍 **Zero Dependencies** | Pure Python standard library, ready to use | ✅ |

### 🚀 Quick Start

#### Requirements

- **Python**: 3.8 or higher
- **OS**: Windows / macOS / Linux

#### Installation

```bash
# Clone repository
git clone https://github.com/gitstq/GitTrendPulse.git
cd GitTrendPulse

# Install (optional, enables global command)
pip install -e .

# Or run directly
python -m gittrendpulse
```

#### Basic Usage

```bash
# View today's trends
gittrendpulse trending

# View Python trends
gittrendpulse trending --language python

# Analyze repository health
gittrendpulse health microsoft/vscode

# Get AI recommendations
gittrendpulse recommend --interests ai,machine-learning,python

# Discover emerging projects
gittrendpulse emerging --language javascript

# Compare multiple repositories
gittrendpulse compare facebook/react vuejs/vue sveltejs/svelte

# Analyze trend patterns
gittrendpulse analyze --language python

# View growth velocity
gittrendpulse velocity torvalds/linux
```

### 📖 Detailed Usage Guide

#### 1. Trend Tracking (trending)

```bash
# View weekly trends
gittrendpulse trending --since weekly

# View monthly trends, limit 20
gittrendpulse trending --since monthly --limit 20

# Output JSON format
gittrendpulse trending --output json
```

#### 2. Health Analysis (health)

Analyze multi-dimensional health metrics:

```bash
gittrendpulse health facebook/react
```

Output includes:
- 💯 Health Score (0-100)
- ⭐ Stars / 🍴 Forks statistics
- ⚡ Activity assessment
- 📋 Issue ratio analysis

#### 3. AI Recommendations (recommend)

Get personalized recommendations based on your interests:

```bash
# Specify interest areas
gittrendpulse recommend --interests "machine-learning,python,data-science"

# Limit recommendation count
gittrendpulse recommend --interests ai --limit 5
```

#### 4. Emerging Trends (emerging)

Discover rapidly growing emerging projects:

```bash
# Discover JavaScript emerging projects
gittrendpulse emerging --language javascript

# Set minimum star count
gittrendpulse emerging --min-stars 100
```

#### 5. Repository Comparison (compare)

Compare metrics across multiple repositories:

```bash
gittrendpulse compare facebook/react vuejs/vue angular/angular
```

#### 6. Trend Pattern Analysis (analyze)

Analyze language distribution and hot topics:

```bash
gittrendpulse analyze --language python
```

#### 7. Growth Velocity Analysis (velocity)

Analyze project growth trends and potential:

```bash
gittrendpulse velocity kubernetes/kubernetes
```

### 💡 Design Philosophy & Roadmap

#### Technical Choices

- **Pure Python Standard Library**: Zero third-party dependencies for maximum compatibility
- **urllib**: Native HTTP client, no requests needed
- **argparse**: Standard CLI parsing
- **unittest**: Standard testing framework

#### Architecture

```
GitTrendPulse/
├── gittrendpulse/
│   ├── __init__.py          # Package init
│   ├── github_api.py        # GitHub API client
│   ├── core.py              # Core analysis engine
│   ├── recommender.py       # AI recommendation engine
│   ├── formatter.py         # Output formatter
│   └── cli.py               # CLI interface
├── tests/                   # Unit tests
├── setup.py                 # Setup config
└── requirements.txt         # Dependencies (empty)
```

#### Roadmap

- [x] v1.0.0 - Core functionality
- [ ] v1.1.0 - Add caching mechanism
- [ ] v1.2.0 - Support HTML report export
- [ ] v1.3.0 - Integrate more data sources
- [ ] v2.0.0 - TUI interactive interface

### 📦 Packaging & Deployment

#### Local Installation

```bash
pip install -e .
```

#### Build Distribution

```bash
python setup.py sdist bdist_wheel
```

#### Install from PyPI (Future)

```bash
pip install gittrendpulse
```

### 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Made with ❤️ by GitTrendPulse Team<br>
  <a href="https://github.com/gitstq/GitTrendPulse">⭐ Star us on GitHub</a>
</p>
