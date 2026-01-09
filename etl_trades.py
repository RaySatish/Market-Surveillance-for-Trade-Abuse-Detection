from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp

spark = SparkSession.builder \
    .appName("MarketSurveillance_ETL") \
    .master("local[*]") \
    .getOrCreate()

print("Spark started")

# Read raw CSV from HDFS directory
input_path = "hdfs:///market/raw/trades/"
print(f"Reading data from {input_path}")

raw_df = spark.read.option("header", True).csv(input_path)

print("Raw count:", raw_df.count())

raw_df.show(5, truncate=False)

clean_df = raw_df \
    .withColumn("price", col("price").cast("double")) \
    .withColumn("quantity", col("quantity").cast("int")) \
    .withColumn("event_time", to_timestamp(col("timestamp"))) \
    .dropna()

print("Clean count:", clean_df.count())

output_path = "hdfs:///market/clean/trades"
print(f"Writing data to {output_path}")

clean_df.write.mode("overwrite").parquet(output_path)

print("ETL COMPLETED SUCCESSFULLY")

spark.stop()
