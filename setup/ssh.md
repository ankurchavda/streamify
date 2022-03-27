## VM SSH Setup

- I recommend watching the first few minutes of [this video by Alexey](https://www.youtube.com/watch?v=ae-CV2KfoN0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb) for understanding how it's done. You can then follow the below steps.

- Create an ssh key in your local system in the `.ssh` folder - [Guide](https://cloud.google.com/compute/docs/connect/create-ssh-keys#linux-and-macos)

- Add the public key (`.pub`) to your VM instance - [Guide](https://cloud.google.com/compute/docs/connect/add-ssh-keys#expandable-2)

- Create a config file in your `.ssh` folder

  ```bash
  touch ~/.ssh/config
  ```

- Copy the following snippet and replace with External IP of the Kafka, Spark (Master Node), Airflow VMs. Username and path to the ssh private key

    ```bash
    Host streamify-kafka
        HostName <External IP Address>
        User <username>
        IdentityFile <path/to/home/.ssh/keyfile>

    Host streamify-spark
        HostName <External IP Address Of Master Node>
        User <username>
        IdentityFile <path/to/home/.ssh/keyfile>

    Host streamify-airflow
        HostName <External IP Address>
        User <username>
        IdentityFile <path/to/home/.ssh/gcp>
    ```

- Once you are setup, you can simply SSH into the servers using the below commands in separate terminals. Do not forget to change the IP address of VM restarts.

    ```bash
    ssh streamify-kafka
    ```

    ```bash
    ssh streamify-spark
    ```

    ```bash
    ssh streamify-airflow
    ```

- You will have to forward ports from your VM to your local machine for you to be able to see Kafka, Airflow UI. Check how to do that [here](https://youtu.be/ae-CV2KfoN0?t=1074)

