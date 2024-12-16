import re
import os
import json
import sys

# Define default values
default_values = {
    "aws_account_id": "123456789012",
    
    "project_name": "DefaultProject",
    "managed_by": "Terraform",
    "aws_region": "eu-west-1",

    "vpc_cidr_range": "10.1.0.0/16",
    "cluster_name": "MyCluster",
    "cluster_version": "1.31",
    "eks_instance_type": "t3.medium",

    "domain_name": "example.com"
}

# Function to replace variables in a file
def replace_vars_in_file(filepath, values):
    with open(filepath, 'r') as file:
        content = file.read()
    
    for key, value in values.items():
        content = re.sub(r'\${' + key + '}', value, content)
    
    with open(filepath, 'w') as file:
        file.write(content)

# Function to recursively find and replace variables in files
def replace_vars_in_directory(directory, values):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.tf') or filename.endswith('.tfvars') or filename.endswith('.yaml'):
                replace_vars_in_file(os.path.join(root, filename), values)

# Load values from a JSON file and merge with default values
def load_values_from_file(values_filepath):
    with open(values_filepath, 'r') as file:
        file_values = json.load(file)
    merged_values = {**default_values, **file_values}
    return merged_values

# Main function to execute the script
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python replace_vars.py <directory> <values_file>")
        sys.exit(1)
    
    directory = sys.argv[1]
    values_filepath = sys.argv[2]
    values = load_values_from_file(values_filepath)
    
    replace_vars_in_directory(directory, values)