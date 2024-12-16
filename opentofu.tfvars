hosted_zones = [
  {
    name        = "${domain_name}"
    environment = "higher"
    is_parent   = true
  },
  {
    name        = "dev.${domain_name}"
    environment = "lower"
    is_parent   = false
  },
  {
    name        = "sit.${domain_name}"
    environment = "lower"
    is_parent   = false
  }
]

lower_tags = {
  Project         = "${project_name}"
  Environment     = "DEV"
  ManagedBy       = "${managed_by}"
  Confidentiality = "C2"
  TaggingVersion  = "V2.4"
  SecurityZone    = "A"
}

higher_tags = {
  Project         = "${project_name}"
  Environment     = "Prod"
  ManagedBy       = "${managed_by}"
  Confidentiality = "C2"
  TaggingVersion  = "V2.4"
  SecurityZone    = "A"
}