variable "uk_hosted_zones" {
  type = list(object({
    name        = string
    environment = string
    is_parent   = bool
  }))
}

variable "lower_tags" {
  type = map(any)
}

variable "higher_tags" {
  type = map(any)
}
