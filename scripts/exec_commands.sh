#Send messages to Kafka Topic from eventsim
docker run -it \
  --network host \
  events:1.0 \
    -c "examples/example-config.json" \
    --start-time "`date +"%Y-%m-%dT%H:%M:%S"`" \
    --end-time "2022-03-18T17:00:00" --nusers 200000 \
    --kafkaBrokerList localhost:9092 \
    --noverbose \
    --continuous

#Stream page view events into Spark
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.3 \
  --deploy-mode cluster \
stream_page_view_events.py

#Stream listen events into Spark
spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.3 \
  --deploy-mode cluster \
stream_listen_events.py