from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.sql import Row
from pyspark import HiveContext, SQLContext, SparkContext, SparkConf
from pyspark.sql.types import StringType,DoubleType,ArrayType,StructType,IntegerType
import pyspark.sql.functions as psf
from pyspark.sql import SparkSession

sc = SparkContext(appName="test" , master="spark://master:7077")
sqlContext = SQLContext(sc)

ratings = sqlContext.read.format("jdbc").options(url=\
        "jdbc:mysql://47.92.101.31:3306/douban?user=liuchenxu&password=Cloud302@",\
        dbtable="comment").load().select(psf.col('id').alias('userId'),psf.col('movie_id').alias('movieId'),psf.col('score').alias('rating'))

(training, test) = ratings.randomSplit([1.0, 0.0])

# Build the recommendation model using ALS on the training data
# Note we set cold start strategy to 'drop' to ensure we don't get NaN evaluation metrics
als = ALS(maxIter=5, regParam=0.01, userCol="userId", itemCol="movieId", ratingCol="rating",
          coldStartStrategy="drop")
model = als.fit(training)


def get_movieId(all_recommend):
    result = ""
    for each in all_recommend:
        result += str(each.movieId) + ","
    return result.strip(',')
test_udf = psf.udf(get_movieId, StringType())
# Generate top 30 movie recommendations for each user
userRecs = model.recommendForAllUsers(30)
userRecs = userRecs.withColumn('one_recommendations', test_udf('recommendations')).\
        select(psf.col('userId').alias('id'), psf.col('one_recommendations').alias('recommend_movie'))
userRecs.write.format("jdbc").options(url="jdbc:mysql://47.92.101.31:3306/liuchenxu_test?user=liuchenxu&password=Cloud302@",\
        dbtable="recommend").mode('append').save()
print(userRecs.take(2))

