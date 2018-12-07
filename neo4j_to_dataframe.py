# -*- coding: utf-8 -*-

from py2neo import Graph
import re
from pandas import DataFrame


class Neo4jToJson(object):
    """知识图谱数据接口"""

    # 与neo4j服务器建立连接
    graph = Graph("http://IP//:7474", username="neo4j", password="xxxxxx")
    links = []
    nodes = []

    def post(self):
        """与前端交互"""
        # 前端传过来的数据
        select_name = '南京审计大学'
        label_name = '单位名称'
        # 取出所有节点数据
        nodes_data_all = self.graph.run("MATCH (n:" + label_name + ") RETURN n").data()
        # node名存储
        nodes_list = []
        for node in nodes_data_all:
            nodes_list.append(node['n']['name'])
        # 根据前端的数据，判断搜索的关键字是否在nodes_list中存在，如果存在返回相应数据，否则返回全部数据
        if select_name in nodes_list:
            # 获取知识图谱中相关节点数据
            links_data = self.graph.run("MATCH (n:" + label_name + "{name:'" + select_name + "'})-[r]-(b) return r").data()
        else:
            # 获取知识图谱中所有节点数据
            links_data = self.graph.run("MATCH ()-[r]->() RETURN r").data()

        data_for_df = self.get_links(links_data)

        # 将列表转换成dataframe
        df = DataFrame(data_for_df, columns=['source', 'name', 'target'])
        return df

    def get_links(self, links_data):
        """知识图谱关系数据获取"""
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
    data_neo4j = Neo4jToJson()
    print(data_neo4j.post())

