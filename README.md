# neo4j-python-pandas-py2neo-v3

利用 pandas 从 Excel 中抽取节点与关系数据，并通过 py2neo v3 写入 Neo4j，用三元组方式构建基础知识图谱。

Utilize pandas to extract nodes and relationships from Excel, then load the triples into Neo4j with py2neo v3 to build a basic knowledge graph.

![](https://s1.ax1x.com/2018/11/13/iObQkn.png)

## Maintenance Status

This project is maintained again as of 2026-06. The current goal is to keep the original py2neo v3 / Neo4j 3.x example usable for learners, notebooks, and legacy projects, while gradually improving documentation, sample data, compatibility notes, and issue triage.

本项目已于 2026-06 恢复维护。当前维护重点是保留原始 py2neo v3 / Neo4j 3.x 示例项目的可运行性，同时逐步补齐文档、样例数据说明、兼容性说明和历史 issue 分类。

## What This Project Does

- Reads invoice-style Excel data with pandas.
- Extracts node data and relationship data from the spreadsheet.
- Creates Neo4j nodes and relationships through py2neo v3.
- Converts Neo4j graph data into matrices for downstream machine learning experiments.

## Compatibility

The original environment was:

- Python 3.6.5
- Windows 10
- Neo4j 3.x
- py2neo 3

The pinned dependencies in `requirements.txt` are intentionally legacy. Modern Python, pandas, Neo4j, and py2neo versions may require code changes. Compatibility modernization is tracked in the roadmap below.

## Quick Start

Install dependencies:

```bash
pip install -r requirements.txt
```

The repository includes `Invoice_data_Demo.xls` as sample data.

Before running `invoice_neo4j.py`, update the local path and Neo4j connection settings:

- Replace `os.chdir('xxxx')` with this repository path, or run the script from the repository root.
- Replace `Graph("http://ip地址//:7474", username="xxx", password="xxx")` in `dataToNeo4jClass/DataToNeo4jClass.py` with your Neo4j server URL and credentials.

## Project Structure

- `invoice_neo4j.py`: reads the Excel file, extracts node and relationship data, and writes to Neo4j.
- `dataToNeo4jClass/DataToNeo4jClass.py`: wraps Neo4j node and relationship creation.
- `neo4j_matrix.py`: extracts Neo4j relationship data and converts it into matrix form.
- `Invoice_data_Demo.xls`: demo Excel data for local testing and learning.
- `requirements.txt`: legacy dependency pins for the original py2neo v3 environment.

## Neo4j Knowledge Graph Construction

### 1. Running Environment

For specific package dependencies, refer to `requirements.txt`.

### 2. Pandas Extraction Of Excel Data

The Excel data structure is as follows:

<img src="https://s1.ax1x.com/2018/11/13/iObTc8.png" width="800" hegiht="500" align=center />

The `data_extraction` and `relation_extraction` functions extract the node data and relationship data required for building the knowledge graph.

`invoice_neo4j.py`

<img src="https://s1.ax1x.com/2018/11/13/iOb4ht.png" width="500" hegiht="313" align=center />

### 3. Establishing Node And Edge Data

`DataToNeo4jClass.py`

<img src="https://s1.ax1x.com/2018/11/13/iXk6iV.png" width="500" hegiht="313" align=center />

`neo4j_matrix.py` extracts knowledge graph data and converts it into matrices for machine learning models.

## Roadmap

### v0.2.x - Restore Maintenance

- Triage historical issues and close resolved sample-data questions.
- Document the known working legacy environment.
- Add clearer setup notes for Windows, local paths, Neo4j credentials, and sample data.
- Publish a maintenance restart release.

### v0.3.x - Reproducible Examples

- Add a minimal end-to-end example that runs from the repository root.
- Replace hard-coded local paths with configurable arguments.
- Add smoke tests for Excel extraction and relationship DataFrame generation.
- Add issue templates for bug reports, compatibility questions, and sample-data requests.

### v0.4.x - Modern Compatibility

- Evaluate support for newer Python and pandas versions.
- Document the migration path from py2neo v3 to newer Neo4j Python tooling.
- Add CI checks for the supported legacy environment where practical.

## Issue Triage

New and historical issues are being reviewed in batches. When opening an issue, please include:

- Python version
- Neo4j version
- py2neo version
- operating system
- the command you ran
- the full error message or screenshot

For sample data questions, use the included `Invoice_data_Demo.xls` file first.

---

# 中文说明

## Neo4j 知识图谱构建

利用 pandas 将 Excel 中数据抽取，以三元组形式加载到 Neo4j 数据库中构建相关知识图谱。

### 1. 运行环境

原始环境：

- Python 3.6.5
- Windows 10
- Neo4j 3.x
- py2neo 3

具体包依赖可以参考 `requirements.txt`。

```bash
pip install -r requirements.txt
```

### 2. Pandas 抽取 Excel 数据

Excel 数据结构如下：

<img src="https://s1.ax1x.com/2018/11/13/iObTc8.png" width="800" hegiht="500" align=center />

通过 `data_extraction` 和 `relation_extraction` 分别抽取构建知识图谱所需要的节点数据以及联系数据，构建三元组。数据提取主要采用 pandas 将 Excel 数据转换成 DataFrame 类型。

### 3. 建立知识图谱所需节点和边数据

`DataToNeo4jClass.py` 负责通过 py2neo 创建节点和关系。

### 4. 矩阵转换

`neo4j_matrix.py` 将知识图谱中的数据抽取并转化成矩阵，为机器学习模型提供数据。
