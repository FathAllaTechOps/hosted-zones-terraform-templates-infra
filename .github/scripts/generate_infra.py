import json
import os
import shutil
import sys

def load_values(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)

def create_infra_dir(base_dir, working_dir, values):
    infra_dir = os.path.join(base_dir, 'infrastructure')
    os.makedirs(infra_dir, exist_ok=True)

    # Copy bootstrap directory
    bootstrap_dir = os.path.join(working_dir, 'bootstrap')
    shutil.copytree(bootstrap_dir, os.path.join(infra_dir, 'bootstrap'), dirs_exist_ok=True)

    # Copy .tf and .tfvars files
    tf_file = os.path.join(working_dir, 'opentofu.tf')
    tfvars_file = os.path.join(working_dir, 'opentofu.tfvars')
    shutil.copy(tf_file, infra_dir)
    shutil.copy(tfvars_file, infra_dir)

    # Update .tfvars file with values from values.json
    tfvars_path = os.path.join(infra_dir, os.path.basename(tfvars_file))
    with open(tfvars_path, 'r') as f:
        tfvars_content = f.read()

    tfvars_content = tfvars_content.replace("${domain_name}", values['environment']['Higher']['domain-names'][1])
    tfvars_content = tfvars_content.replace("${project_name}", values['project_name'])
    tfvars_content = tfvars_content.replace("${managed_by}", values['managed_by'])

    with open(tfvars_path, 'w') as f:
        f.write(tfvars_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_infra.py <values.json> <working_dir>")
        sys.exit(1)

    values_file = sys.argv[1]
    working_dir = sys.argv[2]

    values = load_values(values_file)
    create_infra_dir(os.path.dirname(values_file), working_dir, values)
