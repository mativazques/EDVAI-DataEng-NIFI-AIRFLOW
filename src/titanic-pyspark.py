from pyspark.sql.session import SparkSession 
from pyspark.sql.functions import avg

spark = SparkSession.builder \
    .appName("titanic ETL") \
    .config("spark.sql.catalog.Implementation", "hive") \
    .enableHiveSupport() \
    .getOrCreate()

df = spark.read.option("header","True").csv("hdfs://172.17.0.2:9000/nifi/titanic.csv")

df_a = df.select(df.PassengerId.cast("integer"), df.Survived.cast("integer"), df.Pclass, df.Name, df.Sex, df.Age.cast("integer"), df.Ticket, df.Fare.cast("float"), df.Cabin, df.Embarked.cast("float"))
df_a.createOrReplaceTempView("vw_df_a")

df_b = spark.sql("select *, avg(Age) over (partition by Sex) as avg_ages from vw_df_a")

df_c = df_b.fillna({"Cabin": 0 })
df_c.write.mode("overwrite").saveAsTable("titanicdb.titanic")