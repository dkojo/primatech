terraform {
  backend "s3" {
    bucket         = "prima-tech-terraform-state"
    key            = "state/prima-api-server.tfstate"
    region         = "us-east-1"
    use_lockfile = true
  }
}

