# -*- coding: utf-8 -*-

from py2neo import Graph


graph = Graph("http://localhost//:7474", username="xxx", password="xxx")

sel_name = '杨宁利'

nodes_name = graph.run("MATCH (n:发票信息)--(b) return n").data()



def info_out(nodes_data):

    print(len(nodes_data))
    invioce_info = []
    for node in nodes_data:
        # 存储每个发票key值
        name = node['b']['name']
        inv_name = node['b']['inv_name']
        machinary_code = node['b']['machinary_code']
        invoice_code = node['b']['invoice_code']
        bill_date = node['b']['bill_date']
        check_code = node['b']['check_code']
        purchaser_name = node['b']['purchaser_name']
        addr_num = node['b']['addr_num']
        seller_name = node['b']['seller_name']
        pur_ident_num = node['b']['pur_ident_num']
        pur_bank = node['b']['pur_bank']
        sale_ident_num = node['b']['sale_ident_num']
        sale_addr = node['b']['sale_addr']
        sale_bank = node['b']['sale_bank']
        proj_name = node['b']['proj_name']
        car_num = node['b']['car_num']
        type_n = node['b']['type_n']
        date_from = node['b']['date_from']
        date_to = node['b']['date_to']
        amont = node['b']['amont']
        tax_rate = node['b']['tax_rate']
        tax = node['b']['tax']
        total_big = node['b']['total_big']
        total_ltt = node['b']['total_ltt']
        payee = node['b']['payee']
        review = node['b']['review']
        issuer = node['b']['issuer']

        dict_invioce = {'发票号码': name.zfill(8), '发票名称': inv_name, '机器编号': machinary_code,
                        '发票代码': invoice_code.zfill(12), '开票日期': bill_date, '校验码': check_code,
                        '购买方名称': purchaser_name, '购买方地址、电话': addr_num, '销售方名称': seller_name,
                        '购买方纳税人识别号': pur_ident_num, '购买方开户行及账号': pur_bank, '销售方纳税人识别号': sale_ident_num,
                        '销售方地址、电话': sale_addr, '销售方开户行及账号': sale_bank, '项目名称': proj_name,
                        '车牌号': car_num, '类型': type_n, '通行日期起': date_from,
                        '通行日期止': date_to, '金额': amont, '税率': tax_rate, '税额': tax, '价税合计（大写）': total_big,
                        '价税合计（小写）': total_ltt, '收款人': payee, '复核': review, '开票人': issuer}

        invioce_info.append(dict_invioce)
        dict_invioce = {}
    return invioce_info


# node名存储
nodes_list = []
for node in nodes_name:
    nodes_list.append(node['n']['name'])
nodes_list = list(set(nodes_list))
print(nodes_list)
# 根据前端的数据，判断搜索的关键字是否在nodes_list中存在，如果存在返回相应数据，否则返回全部数据
if sel_name in nodes_list:
    nodes_data = graph.run("MATCH (n{name:'" + sel_name + "'})--(b) return b").data()
elif sel_name == '空':
    nodes_data = graph.run("MATCH (b:发票号码) return b").data()
else:
    nodes_data = []
info_out(nodes_data)
print(info_out(nodes_data))