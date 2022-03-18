#Run the script using the following command 
# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.3 stream_taxi_json.py

import os
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StringType, FloatType, TimestampType, StructField, StructType
from pyspark.sql.functions import from_json, col, expr, struct

KAFKA_ADDRESS = os.getenv("KAFKA_ADDRESS", 'localhost')

spark = SparkSession \
    .builder \
    .appName("Stream Taxi Data") \
    .getOrCreate()


taxi_rides = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", f"{KAFKA_ADDRESS}:9092") \
    .option("subscribe", "yellow_taxi_ride.json") \
    .load()

taxi_rides = taxi_rides.selectExpr("CAST(value AS STRING)")

taxi_schema = StructType([
    StructField("vendorId", StringType(), True),
    StructField("passenger_count", IntegerType(), True),
    StructField("trip_distance", FloatType(), True),
    StructField("pickup_location", IntegerType(), True),
    StructField("dropoff_location", IntegerType(), True),
    StructField("payment_type", IntegerType(), True),
    StructField("total_amount", FloatType(), True),
    StructField("pickup_datetime", TimestampType(), True)
])

taxi_rides = taxi_rides.select(from_json(col("value"), taxi_schema).alias("data")).select("data.*")

taxi_rides \
    .writeStream \
    .format("console") \
    .outputMode("append") \
    .start() \
    .awaitTermination()