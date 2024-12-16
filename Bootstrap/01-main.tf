module "bootstrap" {
  # checkov:skip=CKV_TF_1: ADD REASON
  source            = "github.com/VFGroup-VBIT/vbitdc-terraform-module-infra.git//Bootstrap?ref=v1.8.1"
  infra_bucket_name = var.infra_bucket_name
  dynamodb_name     = var.dynamodb_name
  tags              = var.tags
}

resource "null_resource" "create_local_file" {
  triggers = {
    always_run = "${timestamp()}"
  }
  provisioner "local-exec" {
    command = <<-EOT
      echo 'terraform {     ' > ../1-backend.tf
      echo 'backend "s3" {  ' >> ../1-backend.tf
      echo 'bucket         = "${module.bootstrap.Infra_Bukcet_name}"' >> ../1-backend.tf
      echo 'region         = "${module.bootstrap.region}"' >> ../1-backend.tf
      echo 'key            = "terraform.tfstate"' >> ../1-backend.tf
      echo 'dynamodb_table = "${module.bootstrap.DynamoDB_name}"' >> ../1-backend.tf
      echo 'profile        = "Default"' >> ../1-backend.tf
      echo '}               ' >> ../1-backend.tf
      echo '}               ' >> ../1-backend.tf
    EOT
  }
  depends_on = [module.bootstrap]
}
