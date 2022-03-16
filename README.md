# Setup

### Terraform

In order to spin up our infra, we will be using Terraform.

```bash
cd terraform
```
```bash
terraform init
```
```bash
terraform apply
```

This should spin up a VPC network and two `n1-standard-2` VM instances. One for Kafka, and one for Spark.

### VM Setup

Create an ssh key in you local system in the `.ssh` folder

```bash
ssh-keygen -t rsa -f ~/.ssh/KEY_FILENAME -C USER -b 2048
```

Add the public key to you VM instance using this [link](https://cloud.google.com/compute/docs/connect/add-ssh-keys)

Create a config file in your `.ssh` folder

```
touch ~/.ssh/config
```

Add the following content in it after replacing with the relevant values below.

```bash
Host streamify-kafka
    HostName <External IP Address>
    User <username>
    IdentityFile <path/to/home/.ssh/gcp>

Host streamify-spark
    HostName <External IP Address>
    User <username>
    IdentityFile <path/to/home/.ssh/gcp>
```

SSH into the server using the below commands in two separate terminals

```bash
ssh streamify-kafka
```
```bash
ssh streamify-spark
```

#### Repo Clone

Clone the git [repo](https://github.com/ankurchavda/streamify) into you VMs 

Run the scripts in VM to install `anaconda`, `docker` and `docker-compose`, `spark` in your VM

```bash
bash scripts/vm_setup.sh username
```
```bash
bash scripts/spark_setup.sh username
```

### Test Kafka-Spark Connection

1. Open the port `9092` on your Kafka server using these [steps](https://stackoverflow.com/a/21068402)
2. Set the environment variable `KAFKA_ADDRESS` to the external IP of your VM machine in both the Spark and the Kafka VM machines:
    ```bash
    export KAFKA_ADDRESS=IP.ADD.RE.SS
    ```
3. Run `docker-compose up` in the `kafka` folder in the Kafka VM.
4. Run the following command in the `kafka/test_connection` folder to start producing -
    ```bash
    python produce_taxi_json.py
    ```
5. Move to the Spark VM and run the following command in the `spark_streaming/test_connection` folder -
    ```bash
    spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.3 stream_taxi_json.py
    ```

## TODO

1. Fix Spark Script with py4j eval
2. Make setup easier with `Makefile`. Possibly a one-click setup.