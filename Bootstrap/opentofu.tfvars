infra_bucket_name = "${project_name}-hostedzones-tfstate"
dynamodb_name     = "${project_name}-hostedzones-state-locking"
tags = {
  Project         = "${project_name}"
  Environment     = "Prod"
  ManagedBy       = "${managed_by}"
  Confidentiality = "C2"
  TaggingVersion  = "V2.4"
  SecurityZone    = "A"
}