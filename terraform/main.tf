terraform {
  required_version = ">=1.0"
  backend "local" {}
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region
  zone    = var.zone
  // credentials = file(var.credentials)  # Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}

# resource "google_compute_network" "vpc_network" {
#   name = "streamify-network"
# }

resource "google_compute_instance" "kafka_vm_instance" {
  name                      = "streamify-kafka-instance"
  machine_type              = "e2-standard-4"
  tags                      = ["kafka"]
  allow_stopping_for_update = true

  boot_disk {
    initialize_params {
      image = var.vm_image
      size  = 30
    }
  }

  network_interface {
    network = var.network
    access_config {
    }
  }
}

resource "google_compute_instance" "spark_vm_instance" {
  name                      = "streamify-spark-instance"
  machine_type              = "n1-standard-2"
  tags                      = ["web", "dev"]
  allow_stopping_for_update = true

  boot_disk {
    initialize_params {
      image = var.vm_image
      size  = 30
    }
  }

  network_interface {
    network = var.network
    access_config {
    }
  }
}

resource "google_storage_bucket" "bucket" {
  name          = "streamify"
  location      = var.region
  force_destroy = true

  uniform_bucket_level_access = true

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 # days
    }
  }
}

resource "google_dataproc_cluster" "spark_cluster" {
  name   = "streamify-spark-cluster"
  region = var.region

  cluster_config {

    gce_cluster_config {
      network = var.network
      zone    = var.zone

      shielded_instance_config {
        enable_secure_boot = true
      }
    }

    staging_bucket = "streamify"

    master_config {
      num_instances = 1
      machine_type  = "e2-medium"
      disk_config {
        boot_disk_type    = "pd-standard"
        boot_disk_size_gb = 40
      }
    }

    software_config {
      image_version = "2.0-debian10"
      override_properties = {
        "dataproc:dataproc.allow.zero.workers" = "true"
      }
      optional_components = ["JUPYTER"]
    }

  }

}