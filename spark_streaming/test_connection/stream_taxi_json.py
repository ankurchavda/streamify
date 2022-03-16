#Run the script using the following command 
# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.3 stream_taxi_json.py

from sqlite3 import Timestamp
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StringType, FloatType, TimestampType, StructField, StructType
from pyspark.sql.functions import from_json, col, expr, struct

spark = SparkSession \
    .builder \
    .appName("Stream Taxi Data") \
    .getOrCreate()


taxi_rides = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "34.134.226.252:9092") \
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


# zones = spark \
#         .readStream \
#         .format("kafka") \
#         .option("kafka.bootstrap.servers", "34.134.226.252:9092") \
#         .option("subscribe", "zones.json") \
#         .load()

# zones = zones.selectExpr("CAST(value AS STRING)")

# zones_schema = StructType([
#     StructField("locationId", StringType(), True),
#     StructField("borough", StringType(), True),
#     StructField("zone", StringType(), True),
#     StructField("service_zone", StringType(), True),
#     StructField("zones_datetime", TimestampType(), True)
# ])

# zones = zones.select(from_json(col("value"), zones_schema).alias("data")).select("data.*")


# # Apply watermarks on event-time columns
# taxi_with_watermark = taxi_rides.withWatermark("pickup_datetime", "1 hours")
# zones_with_watermark = zones.withWatermark("zones_datetime", "1 hours")


# #set interval and join conditions
# join_stream = taxi_with_watermark.join(
#   zones_with_watermark,
#   expr("""
#     pickup_location = locationId AND
#     zones_datetime >= pickup_datetime AND
#     zones_datetime <= pickup_datetime + interval 1 hour
#     """)
# )

# # write back to Kafka
# join_stream \
#     .selectExpr("CAST(vendorId AS STRING) as key", "to_json(struct(*)) AS value") \
#     .writeStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", "localhost:9092") \
#     .option("topic", "spark.stream.join") \
#     .option("checkpointLocation", "checkpoint/") \
#     .outputMode("append") \
#     .start() \
#     .awaitTermination()

#write to a csv
# join_stream \
#     .coalesce(1) \
#     .writeStream \
#     .format("csv") \
#     .option("path", "../avro/data/stream_output/") \
#     .option("checkpointLocation", "checkpoint/") \
#     .outputMode("append") \
#     .start() \
#     .awaitTermination()