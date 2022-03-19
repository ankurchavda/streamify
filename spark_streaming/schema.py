from socket import inet_ntoa
from pyspark.sql.types import IntegerType, StringType, DecimalType, TimestampType, StructField, StructType, LongType, BooleanType

listen_events_schema = StructType([
    StructField("artist", StringType(), True),
    StructField("song", StringType(), True),
    StructField("duration", DecimalType(), True),
    StructField("ts", LongType(), True),
    StructField("sessionid", IntegerType(), True),
    StructField("auth", StringType(), True),
    StructField("level", StringType(), True),
    StructField("itemInSession", IntegerType(), True),
    StructField("city", StringType(), True),
    StructField("zip", IntegerType(), True),
    StructField("state", StringType(), True),
    StructField("userAgent", StringType(), True),
    StructField("lon", DecimalType(), True),
    StructField("lat", DecimalType(), True),
    StructField("userId", LongType(), True),
    StructField("lastName", StringType(), True),
    StructField("firstName", StringType(), True),
    StructField("gender", StringType(), True),
    StructField("registration", LongType(), True)
])

page_view_events_schema = StructType([
    StructField("ts", LongType(), True),
    StructField("sessionId", IntegerType(), True),
    StructField("page", StringType(), True),
    StructField("auth", StringType(), True),
    StructField("method", StringType(), True),
    StructField("status", IntegerType(), True),
    StructField("level", StringType(), True),
    StructField("itemInSession", IntegerType(), True),
    StructField("city", StringType(), True),
    StructField("zip", IntegerType(), True),
    StructField("state", StringType(), True),
    StructField("userAgent", StringType(), True),
    StructField("lon", DecimalType(), True),
    StructField("lat", DecimalType(), True),
    StructField("userId", IntegerType(), True),
    StructField("lastName", StringType(), True),
    StructField("firstName", StringType(), True),
    StructField("gender", StringType(), True),
    StructField("registration", LongType(), True),
    StructField("artist", StringType(), True),
    StructField("song", StringType(), True),
    StructField("duration", DecimalType(), True)
])


auth_events_schema = StructType([
    StructField("ts", LongType(), True),
    StructField("sessionId", IntegerType(), True),
    StructField("level", StringType(), True),
    StructField("itemInSession", IntegerType(), True),
    StructField("city", StringType(), True),
    StructField("zip", IntegerType(), True),
    StructField("state", StringType(), True),
    StructField("userAgent", StringType(), True),
    StructField("lon", IntegerType(), True),
    StructField("lat", IntegerType(), True),
    StructField("userId", IntegerType(), True),
    StructField("lastName", StringType(), True),
    StructField("firstName", StringType(), True),
    StructField("gender", StringType(), True),
    StructField("registration", LongType(), True),
    StructField("success", BooleanType(), True)
])
