# Setup

### Pre-requisites

- Google Cloud Platform Account. 
  - **Note**: You will be charged for all the infra setup. Please avail the $300 credits by creating a new account on GCP.
  - `gcloud` sdk in your local machine.
  - You service account key
- Terraform

### Terraform

Clone the repository in your local machine.

```bash
git clone https://github.com/ankurchavda/streamify.git && \
cd streamify/terraform
```

Spin up the Infra using.

- Initiate terraform and download the required dependencies-
  ```bash
  terraform init
  ```
- View the Terraform plan  
  You will be asked to enter two values, the name of your GCS bucket you want to create and the GCP Project ID. Use the same values everytime (on `terraform apply` too). 
  ```bash
  terraform plan
  ```
- Terraform plan should show the creation of following services -
  - `e2-standard-4` Compute Instance for Kafka
  - `e2-standard-4` Compute Instance for Airflow
  - Dataproc Spark Cluster
    - 1 `e2-standard-2` Master node
    - 2 `e2-medium` Worker nodes
  - A Google Cloud Storage bucket
  - 2 Bigquery Datasets
    - streamify_stg
    - streamify_prod

- Apply the infra
  ```bash
  terraform apply
  ```

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

Host streamify-airflow
    HostName <External IP Address>
    User <username>
    IdentityFile <path/to/home/.ssh/gcp>
```

SSH into the servers using the below commands in separate terminals

```bash
ssh streamify-kafka
```
```bash
ssh streamify-spark
```
```bash
ssh streamify-airflow
```

### Setup Kafka VM

- Clone git repo and cd into Kafka folder
  ```bash
  git clone https://github.com/ankurchavda/streamify.git && \
  ```
- Install anaconda, docker & docker-compose.
  ```bash
  bash ~/streamify/scripts/vm_setup.sh && \
  exec newgrp docker
  ```

- Set the evironment variables -
  - External IP of the Kafka VM
  - GCP Project ID
  - Cloud Storage Bucket
    ```bash
    export KAFKA_ADDRESS=IP.ADD.RE.SS
    export GCP_PROJECT_ID=project-id
    export GCP_GCS_BUCKET=bucket-name
    ```

- Start Kafka 
  ```bash
  cd ~/streamify/kafka && \
  docker-compose up 
  ```
  **Note**: Sometimes the `broker` & `schema-registry` containers die during startup. You should just stop all the containers and then rerun `docker-compose up`.

- Open another terminal session for the Kafka VM and start sending messages to your Kafka broker with Eventsim
  ```bash
  bash ~/streamify/scripts/eventsim_startup.sh
  ```
  This will start events for 1 Million users spread out from the current time to the next 24 hours. Follow the logs to see the progress.

- To follow the logs
  ```bash
  docker logs --follow million_events
  ```
  
### Setup Airflow VM

- Clone git repo, update and install make

    ```bash
    git clone https://github.com/ankurchavda/streamify.git && \
    cd streamify
    ```
- Move the `google_credentials.json` file to `~/.google/credentials/` in your VM. Else the dags will fail.

- Install anaconda, docker & docker-compose.

    ```bash
    bash ~/streamify/scripts/vm_setup.sh && \
    exec newgrp docker
    ```

- Set the evironment variables -
  - GCP Project ID
  - Cloud Storage Bucket
    ```bash
    export GCP_PROJECT_ID=project-id
    export GCP_GCS_BUCKET=bucket-name
    ```
  **Note**: You will have setup these env vars every time you create a shell session.

- Start Airflow. (This shall take a few good minutes, grab a coffee!)
  ```bash
  bash ~/streamify/scripts/airflow_startup.sh && cd ~/streamify/airflow
  ```
- Follow the docker-compose logs
  ```bash
  docker-compose --follow
  ```
- Airflow should be available on port `8080`. Login with default username & password as **airflow**.

## TODO

1. Change lat/lon values to decimal
2. Make setup easier with `Makefile`. Possibly a one-click setup.
3. Setup the entire cluster with Terraform - Open network ports, create target tags.
4. Object-oriented design for spark streaming. 