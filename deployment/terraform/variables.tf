variable "name" {
  type        = string
  description = "The name of the cluster"
  default     = "eks-cluster-managed-node-groups"
}

variable "environment" {
  type        = string
  description = "The environment of the cluster"
  default     = "dev"
}

variable "cluster_version" {
  type        = string
  description = "The version of the cluster"
  default     = "1.24"
}

variable "region" {
  type        = string
  description = "The region of the cluster"
  default     = "eu-central-1"
}

variable "vpc_cidr" {
  type        = string
  description = "The CIDR of the VPC"
  default     = "10.0.0.0/16"
}

variable "default_tags" {
  type        = map(string)
  description = "The default tags of the cluster"
  default = {
    ProvisionedBy = "Terraform"
  }
}
