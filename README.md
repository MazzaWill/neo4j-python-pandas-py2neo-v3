# neo4j-python-pandas-py2neo-v3
Utilize pandas to extract data from Excel and load it into the Neo4j database in triplet form to construct a relevant knowledge graph.
![](https://s1.ax1x.com/2018/11/13/iObQkn.png)
## Neo4j Knowledge Graph Construction
### 1. Running Environment:
python3.6.5
windows10
For specific package dependencies, refer to the requirements.txt file.

pip install -r requirements.txt
### 2. Pandas Extraction of Excel Data
The Excel data structure is as follows:

<img src="https://s1.ax1x.com/2018/11/13/iObTc8.png" width="800" hegiht="500" align=center />

The data_extraction and relation_extrantion functions are used to extract the node data and relationship data required for building the knowledge graph, respectively, to construct triplets.
Data extraction primarily uses pandas to convert Excel data into a DataFrame type.
invoice_neo4j.py
<img src="https://s1.ax1x.com/2018/11/13/iOb4ht.png" width="500" hegiht="313" align=center />

### 3. Establishing Node and Edge Data for the Knowledge Graph
DataToNeo4jClass.py
<img src="https://s1.ax1x.com/2018/11/13/iXk6iV.png" width="500" hegiht="313" align=center />

Update neo4j_matrix.py code to extract and convert knowledge graph data into a matrix, providing data for machine learning models.

# neo4j-python-pandas-py2neo-v3
利用pandas将excel中数据抽取，以三元组形式加载到neo4j数据库中构建相关知识图谱
# Neo4j知识图谱构建
![](https://s1.ax1x.com/2018/11/13/iObQkn.png)

### 1.运行环境：  
python3.6.5  
windows10  
具体包依赖可以参考文件requirements.txt
```
pip install -r requirements.txt
``` 

### 2.Pandas抽取excel数据
Excel数据结构如下

<img src="https://s1.ax1x.com/2018/11/13/iObTc8.png" width="800" hegiht="500" align=center />

通过函数data_extraction和函数relation_extrantion分别抽取构建知识图谱所需要的节点数据以及联系数据，构建三元组。  
数据提取主要采用pandas将excel数据转换成dataframe类型    
invoice_neo4j.py  
<img src="https://s1.ax1x.com/2018/11/13/iOb4ht.png" width="500" hegiht="313" align=center />

### 3.建立知识图谱所需节点和边数据  
DataToNeo4jClass.py  
<img src="https://s1.ax1x.com/2018/11/13/iXk6iV.png" width="500" hegiht="313" align=center />


### 更新neo4j_matrix.py代码，将知识图谱中数据抽取转化成矩阵，为机器学习模型提供数据
