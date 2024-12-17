import json
import os
import shutil
import sys
import glob

def load_values(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)

def replace_placeholders(file_path, values):
    with open(file_path, 'r') as f:
        content = f.read()

    # Replace placeholders
    content = content.replace("${project_name}", values['project_name'])
    content = content.replace("${managed_by}", values['managed_by'])
    content = content.replace("${aws_region}", values['aws_region'])

    # Write back the updated content
    with open(file_path, 'w') as f:
        f.write(content)

def create_infra_dir(base_dir, working_dir, values):
    infra_dir = os.path.join(base_dir, 'infrastructure')
    os.makedirs(infra_dir, exist_ok=True)

    # Copy bootstrap directory
    bootstrap_dir = os.path.join(working_dir, 'bootstrap')
    shutil.copytree(bootstrap_dir, os.path.join(infra_dir, 'bootstrap'), dirs_exist_ok=True)

    # Discover and copy .tf and .tfvars files
    tf_files = glob.glob(os.path.join(working_dir, '*.tf'))
    tfvars_files = glob.glob(os.path.join(working_dir, '*.tfvars'))

    for tf_file in tf_files:
        dest_file = shutil.copy(tf_file, infra_dir)
        replace_placeholders(dest_file, values)

    for tfvars_file in tfvars_files:
        dest_file = shutil.copy(tfvars_file, infra_dir)
        replace_placeholders(dest_file, values)

        # Update .tfvars file with hosted_zones sections
        with open(dest_file, 'r') as f:
            tfvars_content = f.read()

        hosted_zones = []
        for env, env_values in values['environment'].items():
            for i, domain in enumerate(env_values['domain-names']):
                hosted_zones.append({
                    "name": domain,
                    "environment": env,
                    "is_parent": env == "Higher" and i == len(env_values['domain-names']) - 1
                })

        hosted_zones_str = ",\n".join([f'  {{\n    name        = "{zone["name"]}"\n    environment = "{zone["environment"]}"\n    is_parent   = {str(zone["is_parent"]).lower()}\n  }}' for zone in hosted_zones])
        tfvars_content = tfvars_content.replace("hosted_zones = [\n  {\n    name        = \"${domain_name}\"\n    environment = \"Higher\"\n    is_parent   = true\n  },\n  {\n    name        = \"dev.${domain_name}\"\n    environment = \"Lower\"\n    is_parent   = false\n  }\n]", f"hosted_zones = [\n{hosted_zones_str}\n]")

        if "Higher" not in values['environment']:
            tfvars_content = tfvars_content.replace("higher_tags = var.higher_tags\n", "")
            tfvars_content = tfvars_content.replace("higher_tags    = var.higher_tags\n", "")

        with open(dest_file, 'w') as f:
            f.write(tfvars_content)

    # Replace placeholders in all files in the infrastructure directory
    for root, _, files in os.walk(infra_dir):
        for file in files:
            file_path = os.path.join(root, file)
            replace_placeholders(file_path, values)

    # Update 2-main.tf file
    main_tf_path = os.path.join(infra_dir, '2-main.tf')
    if os.path.exists(main_tf_path):
        with open(main_tf_path, 'r') as f:
            main_tf_content = f.read()

        if "Higher" not in values['environment']:
            main_tf_content = main_tf_content.replace('  higher_profile = "Higher"\n', '')
            main_tf_content = main_tf_content.replace('  higher_tags    = var.higher_tags\n', '')

        with open(main_tf_path, 'w') as f:
            f.write(main_tf_content)

    # Update 3-variables.tf file
    variables_tf_path = os.path.join(infra_dir, '3-variables.tf')
    if os.path.exists(variables_tf_path):
        with open(variables_tf_path, 'r') as f:
            variables_tf_content = f.read()

        if "Higher" not in values['environment']:
            variables_tf_content = variables_tf_content.replace('variable "higher_tags" {\n  description = "Tags for higher environment"\n  type        = map(string)\n}\n\n', '')

        with open(variables_tf_path, 'w') as f:
            f.write(variables_tf_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_infra.py <values.json> <working_dir>")
        sys.exit(1)

    values_file = sys.argv[1]
    working_dir = sys.argv[2]

    values = load_values(values_file)
    create_infra_dir(os.path.dirname(values_file), working_dir, values)
