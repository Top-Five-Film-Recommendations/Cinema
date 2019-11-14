# 用于上传mysql
import pymysql
import numpy as np
import MySQLdb
import random

si = 18

matrix = np.random.random(size = (si,si))
matrix = np.triu(matrix)
matrix += matrix.T - np.diag(matrix.diagonal())

db = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='xt032341',
    db='cinema',
    use_unicode=True,
    charset="utf8"
)

cur = db.cursor()

index =0
for i in range(1,si+1):
    for j in range(1,si+1):
        index += 1
        sql = "INSERT INTO movie_moviesimilar (id,item1,item2,similar) VALUES({},{},{},{});".format(int(index),int(i),int(j),float(matrix[i-1][j-1]))
        cur.execute(sql)
        db.commit()





