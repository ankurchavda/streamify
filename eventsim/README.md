## Eventsim

Eventsim is a program that generates event data to replicate page requests for a fake music web site (picture something like Spotify); the results look like real use data, but are totally fake. You can find the original repo [here](https://github.com/Interana/eventsim). My docker image is borrowed from [viirya's clone](https://github.com/viirya/eventsim) of it, as the original project has gone without maintenance for a few years now.

### Setup

#### Docker Image
```bash
docker build -t events:1.0 .
```

#### Run With Kafka Configured On Localhost
```bash
docker run -it \
  --network host \
  events:1.0 \
    -c "examples/example-config.json" \
    --start-time "`date +"%Y-%m-%dT%H:%M:%S"`" \
    --end-time "2022-03-18T17:00:00" --nusers 20000 \
    --kafkaBrokerList localhost:9092 \
    --continuous
```