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

resource "google_compute_instance" "vm_instance" {
  name                      = "streamify-kafka-instance"
  machine_type              = "n1-standard-2"
  tags                      = ["web", "dev"]
  allow_stopping_for_update = true

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
      size  = 30
    }
  }

  network_interface {
    network = "default"
    access_config {
    }
  }
}