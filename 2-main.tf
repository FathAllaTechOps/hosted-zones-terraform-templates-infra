module "hosted_zones" {
  source         = "github.com/VFGroup-VBIT/vbitdc-terraform-module-infra.git//Hosted_Zone?ref=v1.4.8"
  hosted_zones   = var.hosted_zones
  lower_profile  = "Lower"
  higher_profile = "Higher"
  lower_tags     = var.lower_tags
  higher_tags    = var.higher_tags
}
