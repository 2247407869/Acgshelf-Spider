# coding: utf-8

import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "testdb")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

id = 1
ranking = 199

sql = "INSERT INTO game_ranking (ID, Ranking) VALUES ('%d', '%d')" % (id, ranking)

try:
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
except:
    # 如果发生错误则回滚
    db.rollback()

# 关闭数据库连接
db.close()