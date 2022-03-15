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

This should spin up a VPC network and an `n1-standard-2` VM instance.

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
    IdentityFile <path/your/google_credentials.json>
```

SSH into the server using 

```bash
ssh streamify-kafka
```

#### Script

In a different terminal, sftp the `vm_setup.sh` [script](scripts/vm_setup.sh) to the VM

```bash
cd scripts
sfpt streamify-kafka 
```
```bash
put vm_setup.sh
```

Run the script in VM to install `anaconda`, `docker` and `docker-compose` iin your VM

```bash
bash vm_setup.sh username
```