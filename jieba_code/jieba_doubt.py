# -*- coding: utf-8 -*-
import jieba
import pymysql


# 连接数据库
conn = pymysql.connect(
    host="xxx",
    user="root",
    passwd="xxx",
    db="shenji",
    charset='utf8')

# 创建游标
cursor = conn.cursor()

doubt_file = "select audit_dbt, audit_con, audit_rec from shenji_audit_doubt "

cursor.execute(doubt_file)

conn.commit()
cursor.close()
conn.close

result = list(cursor.fetchall())
# df = pd.DataFrame(result)
# print(df)

# userword = '''如果应付票据超过其付款期限，可能出现的问题包括利用“应付票据”账户，转移收入；购销双方存在经济纠纷；付款单位无力支付货款'''

f = open("./doubt.txt")
list_wordlist = f.readline().strip(" '").split("','")
# 列表去重
list_wordlist = list(set(list_wordlist))

# print(list_wordlist, len(list_wordlist))

'''
以三元组形式存入mysql中
1.jieba分词文本doubt.txt，找出关键词
2.遍历关键词是否与审计疑点文本有关联，找出相关的审计疑点关键词，存入列表doubt_list
3.审计疑点关键词与审计结论，审计建议建立关系映射（三元组）存入MySQL
'''
# 连接数据库
conn = pymysql.connect(
    host="xxx",
    user="root",
    passwd="xxx",
    db="invioce_info",
    charset='utf8')
# 创建游标
cursor = conn.cursor()

for doubt in result:
    # 疑点列表
    doubt_list = []
    for line in list_wordlist:
        # 结巴分词，找出相关审计疑点
        for word in jieba.lcut(line.strip().replace('\n', '').replace('　', '')):
            if word in doubt[0] and len(word) > 1:
                doubt_list.append(line)
    # 去重
    doubt_list = list(set(doubt_list))
    audit_map = []
    for map in doubt_list:
        audit_doubt = map
        audit_con = doubt[1]
        audit_rc = doubt[2]

        # sql语句
        sql = "insert into shenji_audit_map(audit_doubt, audit_con, audit_rc)" \
              " values ('{}','{}','{}');" \
            .format(audit_doubt, audit_con, audit_rc)

        list_data = [audit_doubt, audit_con, audit_rc]

        cursor.execute(sql)

        # audit_map = [map, doubt[1], doubt[2]]
        # print(audit_map)
    # print(doubt_list, "\n", len(doubt_list))

conn.commit()
cursor.close()
conn.close

