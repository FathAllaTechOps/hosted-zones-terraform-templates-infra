variable "infra_bucket_name" {
  type = string
}
variable "dynamodb_name" {
  type = string
}
variable "tags" {
  description = "Tags to set on the bucket."
  type        = map(string)
}