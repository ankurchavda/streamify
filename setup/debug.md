## Debug Guide

### General Guidelines

- Always make sure the ENV variables are set
- Start the processes in this order - Kafka -> Eventsim -> Spark Streaming -> Airflow
- Monitor the CPU utilization for your VMs to see if something's wrong

### Kafka
- Sometimes the `broker` & `schema-registry` containers die during startup, so the control center might not be available over 9021. You should just stop all the containers with `docker-compose down` or `ctrl+C` and then rerun `docker-compose up`.
- Did not set the `KAFKA_ADDRESS` env var. Kafka will then write to localhost, which will not allow Spark to read messages.

### Eventsim
- If you start with a high number of users - 2-3 Million+, then eventsim sometimes might not startup and get stuck at generating events. Lower the number of users. Start two parallel processes with users divided.
### Spark

- > Connection to node -1 (localhost/127.0.0.1:9092) could not be established. Broker may not be available.
  
  Make sure that the `KAFKA_ADDRESS` env variable is set with the external IP Address of the Kafka VM. If it's set and things still don't seem to work, restart the cluster :/.

### Airflow

- Permission denied to dbt for writing logs
  - The `airflow_startup.sh` handles changing permission for the dbt folder, so you should be good. In case you happen to delete and recreate the folder, or not run the `airflow_startup.sh` script in the first place, then change the dbt folder permissions manually -
    ```bash
    sudo chmod -R 777 dbt/
    ```