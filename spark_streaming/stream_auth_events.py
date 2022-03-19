# Run the script using the following command
# spark-submit \
# --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.3 \
# --deploy-mode cluster \
# stream_auth_events.py

import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, month, hour, dayofmonth, col, year
from schema import auth_events_schema

KAFKA_ADDRESS = os.getenv("KAFKA_ADDRESS", 'localhost')

# will raise error if env variable not found
GCS_STORAGE_PATH = os.environ["GCS_STORAGE_PATH"]

# initialize a spark session
spark = (SparkSession
         .builder
         .appName("Auth View Events")
         .master("yarn")
         .getOrCreate())


# auth view stream
auth_events = (spark
                 .readStream
                 .format("kafka")
                 .option("kafka.bootstrap.servers", f"{KAFKA_ADDRESS}:9092")
                 .option("startingOffsets", "earliest")
                 .option("subscribe", "auth_events")
                 .load())

# read only value from the incoming message and convert the contents
# inside to the passed schema
auth_events = (auth_events
                .selectExpr("CAST(value AS STRING)")
                .select(
                    from_json(col("value"), auth_events_schema).alias("data")
                    )
                .select("data.*")
                )

# Add month, day, hour to split the data into separate directories
auth_events = (auth_events
                 .withColumn("ts", (col("ts")/1000).cast("timestamp"))
                 .withColumn("year", year(col("ts")))
                 .withColumn("month", month(col("ts")))
                 .withColumn("hour", hour(col("ts")))
                 .withColumn("day", dayofmonth(col("ts")))
                 )

(auth_events
    .writeStream
    .format("parquet")
    .partitionBy("month", "day", "hour")
    .option("path", f"{GCS_STORAGE_PATH}/auth_events/")
    .option("checkpointLocation", f"{GCS_STORAGE_PATH}/cp_auth_events/")
    .trigger(processingTime='120 seconds')
    .outputMode("append")
    .start()
    .awaitTermination())