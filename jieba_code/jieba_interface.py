# -*- coding: utf-8 -*-
import pymysql

# 连接数据库
conn = pymysql.connect(
    host="115.xx.107.xx",
    user="rootxxx",
    passwd="rootxx",
    db="shenji",
    charset='utf8')

doubt_tag = '预提费用'
# 创建游标
cursor = conn.cursor()
sql = "select audit_con, audit_rc from shenji_audit_map where audit_doubt='"+doubt_tag+"'"
doubt_file = sql
print(doubt_file)
cursor.execute(doubt_file)

conn.commit()
cursor.close()
conn.close

result = list(cursor.fetchall())
print(result)

result_list = []
result_dict = {}
for line in result:
    result_dict['审计建议'] = line[1]
    result_dict['审计结论'] = line[0]
    result_dict['审计疑点'] = doubt_tag
    result_list.append(result_dict)
    result_dict = {}
print(result_list)
