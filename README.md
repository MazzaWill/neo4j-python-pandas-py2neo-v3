# neo4j-python-pandas-py2neo-v3

[![Release](https://img.shields.io/github/v/release/MazzaWill/neo4j-python-pandas-py2neo-v3)](https://github.com/MazzaWill/neo4j-python-pandas-py2neo-v3/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/maintenance-active-brightgreen.svg)](https://github.com/MazzaWill/neo4j-python-pandas-py2neo-v3/issues/23)

English | [Simplified Chinese](README.zh-CN.md)

Extract nodes and relationships from Excel with pandas, then load the triples into Neo4j through py2neo v3 to build a basic knowledge graph.

![](https://s1.ax1x.com/2018/11/13/iObQkn.png)

## Maintenance Status

This project is maintained again as of 2026-06. The current goal is to keep the original py2neo v3 / Neo4j 3.x example usable for learners, notebooks, and legacy projects while improving documentation, sample data guidance, compatibility notes, and issue triage.

This repository is intentionally maintained as a legacy educational example. Modern Python, pandas, Neo4j, and py2neo versions may require code changes; modernization work is tracked separately so the legacy baseline remains clear.

## What This Project Does

- Reads invoice-style Excel data with pandas.
- Extracts node data and relationship data from the spreadsheet.
- Creates Neo4j nodes and relationships through py2neo v3.
- Converts Neo4j graph data into matrices for downstream machine learning experiments.

## Compatibility

The original working environment was:

- Python 3.6.5
- Windows 10
- Neo4j 3.x
- py2neo 3

The pinned dependencies in `requirements.txt` are intentionally legacy. Dependency and security modernization is tracked in [issue #23](https://github.com/MazzaWill/neo4j-python-pandas-py2neo-v3/issues/23).

## Quick Start

Install dependencies:

```bash
pip install -r requirements.txt
```

The repository includes `Invoice_data_Demo.xls` as sample data.

Before running `invoice_neo4j.py`, update the local path and Neo4j connection settings:

- Replace `os.chdir('xxxx')` with this repository path, or run the script from the repository root.
- Replace the placeholder `Graph(...)` connection in `dataToNeo4jClass/DataToNeo4jClass.py` with your Neo4j server URL and credentials.

## Project Structure

- `invoice_neo4j.py`: reads the Excel file, extracts node and relationship data, and writes to Neo4j.
- `dataToNeo4jClass/DataToNeo4jClass.py`: wraps Neo4j node and relationship creation.
- `neo4j_matrix.py`: extracts Neo4j relationship data and converts it into matrix form.
- `Invoice_data_Demo.xls`: demo Excel data for local testing and learning.
- `requirements.txt`: legacy dependency pins for the original py2neo v3 environment.
- `.github/ISSUE_TEMPLATE/`: issue templates for bugs, compatibility questions, and sample-data requests.

## Neo4j Knowledge Graph Construction

### 1. Running Environment

For package dependencies, refer to `requirements.txt`.

### 2. Extracting Excel Data With Pandas

The Excel data structure is as follows:

<img src="https://s1.ax1x.com/2018/11/13/iObTc8.png" width="800" hegiht="500" align=center />

The `data_extraction` and `relation_extraction` functions extract the node data and relationship data required for building the knowledge graph.

`invoice_neo4j.py`

<img src="https://s1.ax1x.com/2018/11/13/iOb4ht.png" width="500" hegiht="313" align=center />

### 3. Creating Nodes And Edges

`DataToNeo4jClass.py`

<img src="https://s1.ax1x.com/2018/11/13/iXk6iV.png" width="500" hegiht="313" align=center />

`neo4j_matrix.py` extracts knowledge graph data and converts it into matrices for machine learning models.

## Roadmap

### v0.2.x - Restore Maintenance

- Triage historical issues and close resolved sample-data questions.
- Document the known working legacy environment.
- Add clearer setup notes for Windows, local paths, Neo4j credentials, and sample data.
- Publish maintenance restart releases.

### v0.3.x - Reproducible Examples

- Add a minimal end-to-end example that runs from the repository root.
- Replace hard-coded local paths with configurable arguments.
- Add smoke tests for Excel extraction and relationship DataFrame generation.
- Improve issue templates based on new bug reports.

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

## Project Governance

- License: [MIT](LICENSE)
- Contributing guide: [CONTRIBUTING.md](CONTRIBUTING.md)
- Security policy: [SECURITY.md](SECURITY.md)
- Support policy: [SUPPORT.md](SUPPORT.md)
- Code of conduct: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- Pull request template: [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md)

Repository maintenance is tracked publicly through issues and releases.
