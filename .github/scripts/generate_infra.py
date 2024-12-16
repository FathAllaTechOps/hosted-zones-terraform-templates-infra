import os
import shutil
import json

def list_directories():
    exclude_dirs = {'.git', '.github'}
    dirs = [d for d in os.listdir('.') if os.path.isdir(d) and d not in exclude_dirs]
    return dirs

def load_values():
    with open('values.json', 'r') as f:
        return json.load(f)

def create_infrastructure_dir():
    infrastructure_dir = 'infrastructure'
    os.makedirs(infrastructure_dir, exist_ok=True)
    return infrastructure_dir

def copy_bootstrap(infrastructure_dir):
    shutil.copytree('Bootstrap', os.path.join(infrastructure_dir, 'Bootstrap'), dirs_exist_ok=True)

def generate_opentofu_tfvars(values, infrastructure_dir):
    hosted_zones = []
    lower_env = values['environment']['Lower']
    for domain in lower_env['domain-names']:
        hosted_zones.append({
            "name": domain,
            "environment": "Lower",
            "is_parent": False
        })
    
    if 'Higher' in values['environment']:
        higher_env = values['environment']['Higher']
        for domain in higher_env['domain-names']:
            hosted_zones.append({
                "name": domain,
                "environment": "Higher",
                "is_parent": domain == higher_env['domain-names'][-1]
            })
    
    opentofu_tfvars_content = f"""
hosted_zones = {json.dumps(hosted_zones, indent=2)}

lower_tags = {{
  Project         = "{values['project_name']}"
  Environment     = "DEV"
  ManagedBy       = "{values['managed_by']}"
  Confidentiality = "C2"
  TaggingVersion  = "V2.4"
  SecurityZone    = "A"
}}

higher_tags = {{
  Project         = "{values['project_name']}"
  Environment     = "Prod"
  ManagedBy       = "{values['managed_by']}"
  Confidentiality = "C2"
  TaggingVersion  = "V2.4"
  SecurityZone    = "A"
}}
"""
    with open(os.path.join(infrastructure_dir, 'opentofu.tfvars'), 'w') as f:
        f.write(opentofu_tfvars_content)

def copy_and_modify_terraform_files(infrastructure_dir, values):
    terraform_files = ['00-backend.tf', '01-providers.tf', '03-data.tf']
    for tf_file in terraform_files:
        shutil.copy(tf_file, os.path.join(infrastructure_dir, tf_file))
    
    provider_content = f"""
provider "aws" {{
  region = "{values['aws_region']}"
}}

terraform {{
  required_providers {{
    aws = {{
      source = "hashicorp/aws"
      version = "~> 5.0"
    }}
  }}
}}
"""
    with open(os.path.join(infrastructure_dir, 'Bootstrap', '00-provider.tf'), 'w') as f:
        f.write(provider_content)

def main():
    values = load_values()
    infrastructure_dir = create_infrastructure_dir()
    copy_bootstrap(infrastructure_dir)
    generate_opentofu_tfvars(values, infrastructure_dir)
    copy_and_modify_terraform_files(infrastructure_dir, values)
    print("Infrastructure directory has been created based on values.json.")

if __name__ == "__main__":
    main()