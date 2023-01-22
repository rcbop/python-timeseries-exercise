locals {
  name            = var.name
  env             = var.environment
  cluster_version = var.cluster_version
  region          = var.region
  vpc_cidr        = var.vpc_cidr

  azs  = slice(data.aws_availability_zones.available.names, 0, 3)
  tags = var.default_tags
}

provider "aws" {
  region = local.region

  default_tags {
    tags = merge(
      var.default_tags,
      {
        Environment = local.env
      },
    )
  }
}

data "aws_availability_zones" "available" {}

################################################################################
# EKS Module
################################################################################

module "eks" {
  source                   = "terraform-aws-modules/eks/aws"
  version                  = "~> 19.0"
  cluster_name             = local.name
  vpc_id                   = module.vpc.vpc_id
  subnet_ids               = module.vpc.private_subnets
  control_plane_subnet_ids = module.vpc.intra_subnets

  cluster_version = "1.24"

  cluster_endpoint_public_access = true

  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
    }
  }

  # EKS Managed Node Group(s)
  eks_managed_node_group_defaults = {
    instance_types = ["t3.small"]
  }

  eks_managed_node_groups = {
    blue = {}
    green = {
      min_size     = 1
      max_size     = 3
      desired_size = 1

      instance_types = ["t3.small"]
      capacity_type  = "SPOT"
    }
  }
}

################################################################################
# Supporting Resources
################################################################################

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 3.0"

  name = local.name
  cidr = local.vpc_cidr

  azs             = local.azs
  private_subnets = [for k, v in local.azs : cidrsubnet(local.vpc_cidr, 4, k)]
  public_subnets  = [for k, v in local.azs : cidrsubnet(local.vpc_cidr, 8, k + 48)]
  intra_subnets   = [for k, v in local.azs : cidrsubnet(local.vpc_cidr, 8, k + 52)]

  enable_ipv6                     = true
  assign_ipv6_address_on_creation = false
  create_egress_only_igw          = true

  public_subnet_ipv6_prefixes  = [0, 1, 2]
  private_subnet_ipv6_prefixes = [3, 4, 5]

  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true

  public_subnet_tags = {
    "kubernetes.io/role/elb" = 1
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = 1
  }
}

resource "aws_ecr_repository" "dashboard_repository" {
  name = "angular-dashboard"
}

resource "aws_ecr_repository" "api_repository" {
  name = "api"
}

resource "aws_ecr_repository" "mqtt_broker_repository" {
  name = "mqtt-broker"
}

resource "aws_ecr_repository" "data_consumer_repository" {
  name = "data-consumer"
}

resource "aws_ecr_repository" "sensor_repository" {
  name = "sensor"
}

resource "aws_ecr_repository" "plotly_dashboard_repository" {
  name = "plotly-dash"
}
