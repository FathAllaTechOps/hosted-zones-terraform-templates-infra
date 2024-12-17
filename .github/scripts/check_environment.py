import json
import os
import sys

# Check if the YAML and JSON file paths are provided
if len(sys.argv) != 3:
    print("Usage: python check_environment.py <path_to_yaml_file> <path_to_json_file>")
    sys.exit(1)

yaml_file_path = sys.argv[1]
json_file_path = sys.argv[2]

# Load the values.json file
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Check if 'Higher' environment exists
if 'Higher' in data['environment']:
    print("Higher environment exists. No changes needed.")
else:
    print("Higher environment does not exist. Modifying main2.yaml...")

    # Read the specified YAML file
    with open(yaml_file_path, 'r') as file:
        lines = file.readlines()

    # Write back to the YAML file excluding the specified sections
    with open(yaml_file_path, 'w') as file:
        skip = False
        for line in lines:
            if 'name: configure Higher aws credentials' in line:
                skip = True
            if 'echo "[Higher]" >> ~/.aws/credentials' in line:
                skip = True
            if skip and line.strip() == '':
                skip = False
                continue
            if not skip:
                file.write(line)
