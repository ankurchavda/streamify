cd ~/streamify/eventsim

echo "Building Eventsim Image..."
docker build -t events:1.0 .

echo "Running Eventsim in detached mode..."
docker run -itd \
  --network host \
  --name million_events \
  --memory="5.5g" \
  --memory-swap="7g" \
  --oom-kill-disable \
  events:1.0 \
    -c "examples/example-config.json" \
    --start-time "`date +"%Y-%m-%dT%H:%M:%S"`" \
    --end-time "`date -d "+1 days" +"%Y-%m-%dT%H:%M:%S"`" \
    --nusers 1000000 \
    --growth-rate 10 \
    --userid 1 \
    --kafkaBrokerList localhost:9092 \
    --randomseed 1 \
    --continuous

echo "Started streaming events for 1 Million users..."
echo "Eventsim is running in detached mode. "
echo "Run 'docker logs --follow million_events' to see the logs."