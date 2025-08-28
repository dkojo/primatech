variable "region" {
  description = "AWS region to deploy resources"
  type        = string
}

variable "bucket_name" {
  description = "S3 bucket name for avatar storage"
  type        = string
}

variable "dynamodb_table" {
  description = "DynamoDB table name for users"
  type        = string
}

variable "eks_cluster_name" {
  type        = string
  description = "Name of the existing EKS cluster"
}

variable "eks_oidc_provider_arn" {
  type        = string
  description = "ARN of the OIDC provider for the EKS cluster"
}

variable "ecr_repository_name" {
  description = "ECR repository name"
  type        = string
}

