terraform {
  backend "s3" {
    bucket         = "cyberhub-higher-hostedzones-tfstate"
    region         = "eu-west-1"
    key            = "terraform.tfstate"
    dynamodb_table = "cyberhub-hostedzones-state-locking"
    profile        = "cyberhub-aws-prod"
  }
}
