# -*- coding: utf-8 -*-
# @Time    : 2019/2/13 13:29
# @Author  : Skyell Wang
# @FileName: neo4j_matrix.py

from py2neo import Graph
import re
import pandas as pd
import numpy as np


class Neo4jToMatrix(object):
    """
    知识图谱数据转换成矩阵类
    1.主体-主体 邻接矩阵
    2.主体-属性
    """
    def __init__(self, select_name, label_name):

        # 与neo4j服务器建立连接
        self.graph = Graph("ip//:7474", username="xxxx", password="xxxx")
        self.links = []
        self.select_name = select_name
        self.label_name = label_name
        # 获取知识图谱中相关节点数据
        links_data = self.graph.run("MATCH (n:" + self.label_name + "{name:'" + self.select_name + "'})-[r]-(b) return r").data()
        # 获取知识图谱中关系数据
        self.data_for_df = self.get_links(links_data)

    def data_handle(self, name1, name2, flag_name):
        """
        数据预处理
        :param name1: 三元组中节点或关系
        :param name2: 三元组中节点或关系
        :param flag_name: 预处理流程标识，如果为'sub',处理主体-主体矩阵；如果为'att'，处理主体-属性矩阵
        :return: 预处理数据
        """
        if flag_name == 'sub':
            # 取出主体并去重
            nod_list = []
            for data in self.data_for_df:
                nod_list.append(data[name1])
                nod_list.append(data[name2])
            # 去重
            nod_list = list(set(nod_list))
            return nod_list
        elif flag_name == 'att':
            name_list = []
            nod_list = []
            for data in self.data_for_df:
                name_list.append(data[name1])
                nod_list.append(data[name2])

            name_list = list(set(name_list))
            nod_list = list(set(nod_list))
            return name_list, nod_list
        else:
            return

    def sub_attrib(self):
        """
        知识图谱三元组数据用户-属性矩阵
        :return: 处理过后的数据
        """
        # 取出数据
        data_neo4j = self.data_handle('name', 'source', flag_name='att')
        name_list = data_neo4j[0]
        nod_list = data_neo4j[1]

        print(nod_list)
        print(name_list)

        lation_list = []
        mid_list = []
        for name in name_list:

            for i in range(0, len(nod_list)):

                for lation in self.data_for_df:

                    if nod_list[i] != name:
                        if name in lation.values() and nod_list[i] in lation.values():
                            mid_list.append(lation['target'])
                            break

                    # 判断是否为最后一个列表元素，如果是最后一个，则赋值NaN,否则继续循环
                    if self.data_for_df.index(lation) == len(self.data_for_df) - 1:
                        mid_list.append('NaN')

            lation_list.append(mid_list)
            mid_list = []
        print(lation_list)

        # 用numpy将列表转成矩阵
        matrix_data = np.array(lation_list).T

        df = pd.DataFrame(matrix_data, columns=name_list, index=nod_list)

        # 将矩阵写入csv格式的文件
        df.to_csv('./data/neo4j_matrix_att.csv', encoding='gbk')
        return df

    def sub_to_sub(self):
        """
        知识图谱三元组数据转邻接矩阵
        :return: 主体-主体 邻接矩阵
        """
        # 取出数据, flag_name:为判断数据初始化方式，如果为'sub'，则为主体-主体；如果为'att',则为主体-属性
        nod_list = self.data_handle('target', 'source', flag_name='sub')

        # 抽取主体与主体间关系矩阵
        lation_list = []
        mid_list = []

        for node_n in nod_list:

            for i in range(0, len(nod_list)):

                for lation in self.data_for_df:
                    # 判断行与列节点名称是否相等，如果不相等则继续
                    if nod_list[i] != node_n:
                        # 判断行列节点是否都在一个三元组中，如果同时存在将关系存入列表
                        if nod_list[i] in lation.values() and node_n in lation.values():
                            mid_list.append(lation['name'])
                            break

                    # 判断是否为最后一个列表元素，如果是最后一个，则赋值NaN,否则继续循环
                    if self.data_for_df.index(lation) == len(self.data_for_df) - 1:
                        mid_list.append('NaN')
            lation_list.append(mid_list)
            mid_list = []
        print(lation_list)
        # 用numpy将列表转成矩阵
        matrix_data = np.array(lation_list)
        print(matrix_data)

        # 将列表转换成dataframe：columns index 指定行列名称；matrix_data 矩阵
        df = pd.DataFrame(matrix_data, columns=nod_list, index=nod_list)
        # 将矩阵写入csv格式的文件
        df.to_csv('./data/neo4j_matrix.csv', encoding='gbk')

        return df

    def get_links(self, links_data):
        """
        知识图谱关系数据获取
        :param links_data: 知识图谱中数据
        :return: 正则处理过的数据
        """
        i = 1
        dict = {}

        # 匹配模式
        pattern = '^\(|\{\}\]\-\>\(|\)\-\[\:|\)$'

        for link in links_data:
            # link_data样式：(南京审计大学) - [: 学校地址{}]->(江苏省南京市浦口区雨山西路86号)
            link_data = str(link['r'])
            # 正则，用split将string切成:['', '南京审计大学', '学校地址 ', '江苏省南京市浦口区雨山西路86号', '']
            links_str = re.split(pattern, link_data)

            for data in links_str:
                if len(data) > 1:
                    if i == 1:
                        dict['source'] = data
                    elif i == 2:
                        dict['name'] = data
                    elif i == 3:
                        dict['target'] = data
                        self.links.append(dict)
                        dict = {}
                        i = 0
                    i += 1
        return self.links


if __name__ == '__main__':
    data_neo4j = Neo4jToMatrix('南京审计大学', '主体')
    data_attribute = Neo4jToMatrix('南京审计大学', '主体')
    print(data_attribute.sub_attrib())
    # print(data_neo4j.sub_to_sub())

