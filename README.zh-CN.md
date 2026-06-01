# Excel to Neo4j Knowledge Graph

[![Release](https://img.shields.io/github/v/release/MazzaWill/neo4j-python-pandas-py2neo-v3)](https://github.com/MazzaWill/neo4j-python-pandas-py2neo-v3/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/maintenance-active-brightgreen.svg)](https://github.com/MazzaWill/neo4j-python-pandas-py2neo-v3/issues/23)

[English](README.md) | 简体中文

从 Excel 发票数据构建 Neo4j 知识图谱的示例仓库：既保留原始 py2neo v3 教学路径，也新增了面向当前应用的 Neo4j GraphRAG/vector-search 路径。

历史仓库名：`neo4j-python-pandas-py2neo-v3`。

![](https://s1.ax1x.com/2018/11/13/iObQkn.png)

## 维护状态

本项目已于 2026-06 恢复维护。当前维护重点是保留原始 py2neo v3 / Neo4j 3.x 示例项目的可运行性，同时新增官方 Neo4j driver、vector index 和 GraphRAG 示例。

本仓库会继续作为 legacy 教学示例维护。现代 Python、pandas、Neo4j、py2neo 版本可能需要代码改造；相关现代化工作会单独跟踪，避免破坏原有 legacy 基线。

## 项目功能

- 使用 pandas 读取发票类 Excel 数据。
- 从表格中抽取节点数据和关系数据。
- 通过 py2neo v3 创建 Neo4j 节点和关系。
- 将 Neo4j 图数据转换为矩阵，供后续机器学习实验使用。

## 现代 Neo4j 示例

仓库现在新增了一个现代化案例：[`examples/modern_invoice_graphrag/`](examples/modern_invoice_graphrag/)。

它保留原项目的发票数据场景，但使用当前 Neo4j 应用栈：

- 官方 `neo4j` Python driver
- Neo4j 5+/2026 vector index
- GraphRAG 风格语义检索
- 可选 `neo4j-graphrag` 生产级 embedding
- 本地 deterministic embedding，便于无 API key demo 和 CI

快速体验：

```bash
python -m examples.modern_invoice_graphrag.app \
  --input examples/modern_invoice_graphrag/sample_invoice_rows.csv \
  --limit 2 \
  dry-run
```

## 开源 Skill

仓库也新增了一个面向 Codex/AI agent 的开源 skill：[`skills/neo4j-knowledge-graph/`](skills/neo4j-knowledge-graph/)。

当 AI coding agent 需要基于 CSV/Excel 设计 Neo4j 知识图谱、生成安全 Cypher、选择 legacy py2neo 或官方 Neo4j driver、或者加入 GraphRAG/vector-search 能力时，可以使用这个 skill。skill 内置了 `profile_table.py`，用于在建模前先分析表格字段。

## 兼容性

原始可运行环境：

- Python 3.6.5
- Windows 10
- Neo4j 3.x
- py2neo 3

`requirements.txt` 中的依赖锁定是有意保留的 legacy 配置。依赖和安全现代化工作集中跟踪在 [issue #23](https://github.com/MazzaWill/neo4j-python-pandas-py2neo-v3/issues/23)。

## 快速开始

安装依赖：

```bash
pip install -r requirements.txt
```

仓库中已经包含样例数据 `Invoice_data_Demo.xls`。

运行 `invoice_neo4j.py` 前，需要修改本地路径和 Neo4j 连接配置：

- 将 `os.chdir('xxxx')` 替换为本仓库路径，或者直接在仓库根目录运行脚本。
- 将 `dataToNeo4jClass/DataToNeo4jClass.py` 中的 `Graph("http://ip地址//:7474", username="xxx", password="xxx")` 替换为你的 Neo4j 服务地址、用户名和密码。

## 项目结构

- `invoice_neo4j.py`: 读取 Excel 文件，抽取节点和关系数据，并写入 Neo4j。
- `dataToNeo4jClass/DataToNeo4jClass.py`: 封装 Neo4j 节点和关系创建逻辑。
- `neo4j_matrix.py`: 从 Neo4j 抽取关系数据并转换成矩阵。
- `Invoice_data_Demo.xls`: 用于本地测试和学习的样例 Excel 数据。
- `requirements.txt`: 原始 py2neo v3 环境的 legacy 依赖锁定。
- `.github/ISSUE_TEMPLATE/`: bug、兼容性问题、样例数据问题的 issue 模板。

## Neo4j 知识图谱构建

### 1. 运行环境

具体包依赖可以参考 `requirements.txt`。

### 2. Pandas 抽取 Excel 数据

Excel 数据结构如下：

<img src="https://s1.ax1x.com/2018/11/13/iObTc8.png" width="800" hegiht="500" align=center />

通过 `data_extraction` 和 `relation_extraction` 分别抽取构建知识图谱所需要的节点数据以及联系数据，构建三元组。数据提取主要采用 pandas 将 Excel 数据转换成 DataFrame 类型。

`invoice_neo4j.py`

<img src="https://s1.ax1x.com/2018/11/13/iOb4ht.png" width="500" hegiht="313" align=center />

### 3. 建立知识图谱所需节点和边数据

`DataToNeo4jClass.py`

<img src="https://s1.ax1x.com/2018/11/13/iXk6iV.png" width="500" hegiht="313" align=center />

`neo4j_matrix.py` 将知识图谱中的数据抽取并转化成矩阵，为机器学习模型提供数据。

## Roadmap

### v0.2.x - 恢复维护

- 分类历史 issue，并关闭已解决的样例数据问题。
- 记录已知可运行的 legacy 环境。
- 补齐 Windows、本地路径、Neo4j 凭据、样例数据等安装说明。
- 发布恢复维护版本。

### v0.3.x - 可复现示例

- 发布现代 Neo4j GraphRAG/vector-search 发票案例。
- 用可配置参数替换硬编码本地路径。
- 为 Excel 抽取和关系 DataFrame 生成增加 smoke test。
- 根据后续 issue 继续改进 issue 模板。

### v0.4.x - 现代兼容性

- 评估新版 Python 和 pandas 的支持情况。
- 记录从 py2neo v3 迁移到新版 Neo4j Python 工具链的路径。
- 在可行的情况下为支持的 legacy 环境增加 CI 检查。

## Issue 分类

新的和历史遗留 issue 会分批处理。提交 issue 时请包含：

- Python 版本
- Neo4j 版本
- py2neo 版本
- 操作系统
- 执行的命令
- 完整错误信息或截图

样例数据问题请先使用仓库内置的 `Invoice_data_Demo.xls`。

## 项目维护

- License: [MIT](LICENSE)
- 贡献指南: [CONTRIBUTING.md](CONTRIBUTING.md)
- 安全策略: [SECURITY.md](SECURITY.md)
- 支持说明: [SUPPORT.md](SUPPORT.md)
- 行为准则: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- PR 模板: [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md)

仓库维护会通过公开 issue 和 release 记录。
