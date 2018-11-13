# -*- coding: utf-8 -*-
from invoice_data.dataToNeo4jClass.DataToNeo4jClass import DataToNeo4j
import os
import pandas as pd


# 提取excel表格中数据，将其转换成dateframe类型
os.chdir('xxxx')

invoice_data = pd.read_excel('./Invoice_data_Demo.xls', header=0, encoding='utf8')
print(invoice_data)


def data_extraction():
    """节点数据抽取"""

    # 取出发票名称到list
    node_list_key = []
    for i in range(0, len(invoice_data)):
        node_list_key.append(invoice_data['发票名称'][i])

    # 去除重复的发票名称
    node_list_key = list(set(node_list_key))

    # value抽出作node
    node_list_value = []
    for i in range(0, len(invoice_data)):
        for n in range(1, len(invoice_data.columns)):
            # 取出表头名称invoice_data.columns[i]
            node_list_value.append(invoice_data[invoice_data.columns[n]][i])
    # 去重
    node_list_value = list(set(node_list_value))
    # 将list中浮点及整数类型全部转成string类型
    node_list_value = [str(i) for i in node_list_value]

    return node_list_key, node_list_value


def relation_extraction():
    """联系数据抽取"""

    links_dict = {}
    name_list = []
    relation_list = []
    name2_list = []

    for i in range(0, len(invoice_data)):
        m = 0
        name_node = invoice_data[invoice_data.columns[m]][i]
        while m < len(invoice_data.columns)-1:
            relation_list.append(invoice_data.columns[m+1])
            name2_list.append(invoice_data[invoice_data.columns[m+1]][i])
            name_list.append(name_node)
            m += 1

    # 将数据中int类型全部转成string
    name_list = [str(i) for i in name_list]
    name2_list = [str(i) for i in name2_list]

    # 整合数据，将三个list整合成一个dict
    links_dict['name'] = name_list
    links_dict['relation'] = relation_list
    links_dict['name2'] = name2_list
    # 将数据转成DataFrame
    df_data = pd.DataFrame(links_dict)
    return df_data


# 实例化对象
data_extraction()
relation_extraction()
create_data = DataToNeo4j()

create_data.create_node(data_extraction()[0], data_extraction()[1])
create_data.create_relation(relation_extraction())
