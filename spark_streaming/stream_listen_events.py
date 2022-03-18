# Run the script using the following command
# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.3 stream_listen_events.py

import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, expr, struct
from schema import listen_events_schema

KAFKA_ADDRESS = os.getenv("KAFKA_ADDRESS", 'localhost')
GCS_STORAGE_PATH = os.environ["GCS_STORAGE_PATH"] #will raise error if env variable not found

spark = (SparkSession
         .builder
         .appName("Listen Events")
         .master("local[*]")
         .getOrCreate())


listen_events = (spark
              .readStream
              .format("kafka")
              .option("kafka.bootstrap.servers", f"{KAFKA_ADDRESS}:9092")
              .option("startingOffsets", "earliest")
              .option("subscribe", "listen_events")
              .load())

listen_events = listen_events.selectExpr("CAST(value AS STRING)")

listen_events = listen_events.select(
    from_json(col("value"), listen_events_schema).alias("data")).select("data.*")

(listen_events
    .writeStream
    .format("parquet")
    .option("path", f"{GCS_STORAGE_PATH}")
    .trigger(processingTime='60 seconds')
    .outputMode("append")
    .start()
    .awaitTermination())
