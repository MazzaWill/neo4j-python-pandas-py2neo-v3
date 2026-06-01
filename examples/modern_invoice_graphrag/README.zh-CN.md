# 现代发票 GraphRAG 示例

[English](README.md) | 简体中文

这个示例把原项目的 “Excel -> Neo4j 知识图谱” 思路升级到当前 Neo4j 应用栈：

- 使用官方 `neo4j` Python driver，而不是 legacy py2neo
- 使用 Neo4j 5+/2026 vector index
- 基于发票记录做 GraphRAG 风格的语义检索
- 可选接入 `neo4j-graphrag` 做生产级 embedding

原来的 py2neo v3 脚本保持不变。本目录是一个新增的现代化案例，适合想基于同一类发票数据继续学习新版 Neo4j 应用的用户。

## 为什么新增这个案例

原项目展示了如何把 Excel 发票数据写入 Neo4j 图数据库。现在 Neo4j 的主流应用方向已经扩展到图结构、向量检索和 GraphRAG 的结合。这个示例展示升级路径，同时不破坏原有 legacy 基线。

## 文件说明

- `model.py`: 将旧版发票表格行规范化为 `InvoiceRecord`。
- `embeddings.py`: 提供本地 deterministic embedding，便于 demo 和测试。
- `cypher.py`: 包含约束、vector index、写入和检索 Cypher。
- `app.py`: 提供 dry-run、load、search CLI。
- `sample_invoice_rows.csv`: 不依赖 pandas 的小样例。
- `requirements-modern.txt`: 现代 Neo4j driver 和 Excel 读取依赖。
- `requirements-graphrag-openai.txt`: 可选生产 GraphRAG embedding 依赖。

## 环境要求

现代 Neo4j 路径：

- Python >=3.10
- Neo4j 5.18+ 或 Neo4j Aura
- `pip install -r examples/modern_invoice_graphrag/requirements-modern.txt`

如果要使用生产级 embedding：

```bash
pip install -r examples/modern_invoice_graphrag/requirements-graphrag-openai.txt
```

默认 deterministic embedder 是本地、无需 key 的 demo 实现，适合测试和 CI，但不是生产级语义 embedding 模型。

## 快速 dry run

不需要 Neo4j，也不需要外部 API：

```bash
python -m examples.modern_invoice_graphrag.app \
  --input examples/modern_invoice_graphrag/sample_invoice_rows.csv \
  --limit 2 \
  dry-run
```

这个命令会输出已经可以写入图数据库的发票 payload 和 deterministic vector。

## 连接 Neo4j 运行

本地启动 Neo4j，例如：

```bash
docker run --rm \
  --name neo4j-invoice-demo \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  neo4j:latest
```

导入样例数据：

```bash
export NEO4J_URI=neo4j://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=password

python -m examples.modern_invoice_graphrag.app \
  --input examples/modern_invoice_graphrag/sample_invoice_rows.csv \
  load
```

检索发票：

```bash
python -m examples.modern_invoice_graphrag.app \
  search "invoice reviewed by Wang Min from Shandong"
```

## 使用原始 Excel 文件

也可以使用仓库根目录的 `Invoice_data_Demo.xls`：

```bash
python -m examples.modern_invoice_graphrag.app \
  --input Invoice_data_Demo.xls \
  --limit 10 \
  dry-run
```

读取 `.xls` 文件需要 pandas 和 `xlrd`。

## 生产 GraphRAG 路径

真实语义检索时，可以把 `DeterministicEmbedding` 替换成 `neo4j-graphrag` 中的 embedding provider，例如 OpenAI embedder。其余流程保持一致：

1. 规范化发票行
2. 构建图 payload
3. 创建约束和 vector index
4. 写入带 embedding 的发票节点
5. 使用 `db.index.vector.queryNodes` 检索

这样既保持案例易懂，也把项目连接到 Neo4j 当前 GraphRAG 生态。

## 官方参考

- Neo4j Python Driver: https://neo4j.com/docs/python-manual/current/
- Neo4j vector indexes: https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/
- Neo4j GraphRAG for Python: https://neo4j.com/docs/neo4j-graphrag-python/current/

## 测试

在仓库根目录执行：

```bash
python -m unittest discover -s tests/modern_invoice_graphrag -v
```
