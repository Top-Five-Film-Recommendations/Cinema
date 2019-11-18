#-*- coding:utf-8 -*-
import pyspark
from pyspark import HiveContext, SQLContext, SparkContext, SparkConf
from pyspark.sql.types import StringType,DoubleType,ArrayType
import pyspark.sql.functions as psf
from pyspark.ml.feature import *
import jieba
from pyspark.ml.feature import OneHotEncoder, StringIndexer
import math
    
def weighted_sim(x1, x2, x3, x4, x5, x6, x7, x8, x9, weighted_x1 = 0.2, weighted_x2 = 0.1, weighted_x3 = 0.1, weighted_x4 = 0.1,\
        weighted_x5 = 0.1, weighted_x6 = 0.1, weighted_x7 = 0.1, weighted_x8 = 0.1, weighted_x9 = 0.1):
    if x9:
        x9 = float(x9)
    else:
        x9 = 0
    return x1 * weighted_x1 + x2 * weighted_x2 + x3 * weighted_x3 + x4 * weighted_x4 + \
            x5 * weighted_x5 + x6 * weighted_x6 + x7 * weighted_x7 + x8 * weighted_x8 + x9 * weighted_x9

def comment_sim(x1, x2):
    if not x1 or not x2:
        return 0
    x1 = {i.split(':')[0]:i.split(':')[1] for i in x1.split(',')}
    x2 = {i.split(':')[0]:i.split(':')[1] for i in x2.split(',')}
    union_key = set(x1.keys()) & set(x2.keys())
    x1_like = 0
    x2_like = 0
    all_like = 0
    for key in union_key:
        if x1[key]=='1':
            x1_like += 1
        if x2[key]=='1':
            x2_like += 1
        if x1[key] == '1' and x2[key] == '1':
            all_like += 1
    if x1_like == 0 or x2_like == 0:
        return 0
    return (all_like)/math.sqrt(x1_like*x2_like)
    


def run_similar(mysql_user, mysql_pwd, mysql_host, mysql_db):

    sc = SparkContext(appName="test" , master="spark://master:7077")
    sqlContext = SQLContext(sc)

    #split udf
    split_udf = psf.udf(lambda x: x.split(), ArrayType(StringType()))

    #seg udf to seg Chinese text
    seg_udf = psf.udf(lambda x: (" ".join(jieba.cut(x))).split(), ArrayType(StringType()))

    # calcu label similarity udf
    equal_udf = psf.udf(lambda x,y: float(x==y), DoubleType())

    # calcu score similarity udf
    score_udf = psf.udf(lambda x,y: math.exp(-(abs(x-y))/2), DoubleType())

    # calcu set similarity udf z is split symptom
    set_udf = psf.udf(lambda x,y,z = " / ": len(set(x.split(z)) & set(y.split(z)))/len(set(x.split(z)) | set(y.split(z))), DoubleType())
    set_udf2 = psf.udf(lambda x,y: len(set(x) & set(y))/len(set(x) | set(y)), DoubleType())
    
    # calcu user comment similarity udf
    user_comment_udf = psf.udf(comment_sim, DoubleType())

    # calcu vector's dot udf
    dot_udf = psf.udf(lambda x,y: (float(x.dot(y))+1.0)/2, DoubleType())
     
    # calcu weighted sim udf
    weighted_udf = psf.udf(weighted_sim)

    # DataFrame from mysql
    df_movieinfo = sqlContext.read.format("jdbc").options(url="jdbc:mysql://47.92.101.31:3306/liuchenxu_test?user=liuchenxu&password=Cloud302@",dbtable="douban_movie").load()
    
    # seg description and calcu normal vector
    df_movieinfo = df_movieinfo.withColumn("split_description", split_udf('description'))
    word2vec_model = Word2Vec(vectorSize=50, seed=42, minCount = 0, inputCol="split_description", outputCol="description_vector").fit(df_movieinfo)
    df_movieinfo = word2vec_model.transform(df_movieinfo)
    normalizer = Normalizer(inputCol="description_vector", outputCol="normal_description_vector", p=2.0)
    df_movieinfo = normalizer.transform(df_movieinfo)
    
    df_movieinfo = df_movieinfo.withColumn("split_name", split_udf('name'))
    word2vec_model_2 = Word2Vec(vectorSize=50, seed=42, minCount = 0, inputCol="split_name", outputCol="name_vector").fit(df_movieinfo)
    df_movieinfo = word2vec_model_2.transform(df_movieinfo)
    normalizer = Normalizer(inputCol="name_vector", outputCol="normal_name_vector", p=2.0)
    df_movieinfo = normalizer.transform(df_movieinfo)

    join_df = df_movieinfo.alias('item1').join(df_movieinfo.alias('item2'), psf.col('item1.id') < psf.col('item2.id')).\
            select(psf.col('item1.id').alias('item1'),\
                   psf.col('item2.id').alias('item2'),\
                   dot_udf('item1.normal_name_vector', 'item2.normal_name_vector').alias('name_sim'),\
                   dot_udf('item1.normal_description_vector', 'item2.normal_description_vector').alias('description_sim'),\
                   equal_udf('item1.directors', 'item2.directors').alias('directors_sim'),\
                   set_udf('item1.leadactors', 'item2.leadactors').alias('leadactors_sim'),\
                   set_udf('item1.nation', 'item2.nation').alias('nation_sim'),\
                   set_udf('item1.language', 'item2.language').alias('language_sim'),\
                   set_udf('item1.editors', 'item2.editors').alias('editors_sim'),\
                   set_udf('item1.type', 'item2.type').alias('type_sim'),\
                   user_comment_udf('item1.comment', 'item2.comment').alias('comment_sim'))
   
    print(join_df.take(1))
    join_df = join_df.select(psf.col('item1'), psf.col('item2'), weighted_udf('name_sim', 'description_sim', 'directors_sim', 'leadactors_sim',\
        'nation_sim', 'language_sim', 'editors_sim', 'type_sim', 'comment_sim').alias('sim'))
    join_df.write.format("jdbc").options(url="jdbc:mysql://47.92.101.31:3306/liuchenxu_test?user=liuchenxu&password=Cloud302@",dbtable="movie_sim").mode('append').save()
    print(join_df.take(1))


    
if __name__ == '__main__':
    run_similar(mysql_user = "liuchenxu",
                mysql_pwd = "Cloud302@",
                mysql_host = "47.92.101.31",
                mysql_db = "liuchenxu_test")

