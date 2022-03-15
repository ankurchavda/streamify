locals {
  data_lake_bucket = "streamify_data_lake"
}

variable "project" {
  description = "Your GCP Project ID"
  default     = "dtc-ny-taxi"
  type        = string
}

variable "region" {
  description = "Your project region"
  default     = "us-central1"
  type        = string
}

variable "zone" {
  description = "Your project zone"
  default     = "us-central1-a"
  type        = string
}

variable "storage_class" {
  description = "Storage class type for your bucket"
  default     = "STANDARD"
}