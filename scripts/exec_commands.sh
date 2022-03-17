#Send messages to Kafka Topic from eventsim
docker run -it \
  --network host \
  events:1.0 \
    -c "examples/example-config.json" \
    --start-time "`date +"%Y-%m-%dT%H:%M:%S"`" \
    --end-time "2022-03-18T17:00:00" --nusers 20000 \
    --kafkaBrokerList localhost:9092 \
    --continuous
