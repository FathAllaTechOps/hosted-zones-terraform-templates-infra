import os
import shutil
import sys

def list_directories():
    exclude_dirs = {'.git', '.github'}
    dirs = [d for d in os.listdir('.') if os.path.isdir(d) and d not in exclude_dirs]
    print("Available modules:")
    for i, d in enumerate(dirs):
        print(f"{i + 1}. {d}")
    return dirs

def get_user_choices(dirs):
    choices = input("Enter the numbers of the modules you need, separated by commas: ")
    choices = [int(choice.strip()) - 1 for choice in choices.split(',')]
    selected_dirs = [dirs[choice] for choice in choices]
    return selected_dirs

def copy_files(src, dest, file_mapping):
    for src_file, dest_file in file_mapping.items():
        src_path = os.path.join(src, src_file)
        dest_path = os.path.join(dest, dest_file)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(src_path, 'r') as src_f, open(dest_path, 'a') as dest_f:
            dest_f.write(src_f.read())

def main(selected_dirs):
    infrastructure_dir = 'infrastructure'
    os.makedirs(infrastructure_dir, exist_ok=True)
    
    default_files = {
        '00-backend.tf': '00-backend.tf',
        '01-providers.tf': '01-providers.tf',
        '03-data.tf': '03-data.tf'
    }
    
    for src_file, dest_file in default_files.items():
        shutil.copy(src_file, os.path.join(infrastructure_dir, dest_file))
    
    shutil.copytree('Bootstrap', os.path.join(infrastructure_dir, 'Bootstrap'), dirs_exist_ok=True)
    
    file_mapping = {
        '1-main.tf': '02-main.tf',
        '2-variables.tf': '04-variables.tf',
        '3-terraform.tfvars': 'Config/Lower.tfvars'
    }
    
    # Copy and append to 04-variables.tf
    variables_file = '04-variables.tf'
    with open(variables_file, 'r') as src_f, open(os.path.join(infrastructure_dir, variables_file), 'a') as dest_f:
        dest_f.write(src_f.read())
    
    for module_dir in selected_dirs:
        copy_files(module_dir, infrastructure_dir, file_mapping)
        if module_dir == 'S3_CloudFront':
            shutil.copytree('CloudFront_Functions', os.path.join(infrastructure_dir, 'CloudFront_Functions'), dirs_exist_ok=True)
        elif module_dir == 'EKS_Config':
            shutil.copytree('Helm_Values', os.path.join(infrastructure_dir, 'Helm_Values'), dirs_exist_ok=True)
    
    print("Infrastructure directory has been created with the selected modules.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        selected_dirs = []
        if sys.argv[1].lower() == 'true':
            selected_dirs.append('S3_CloudFront')
        if sys.argv[2].lower() == 'true':
            selected_dirs.append('Network')
        if sys.argv[3].lower() == 'true':
            selected_dirs.append('EKS_Config')
        if sys.argv[4].lower() == 'true':
            selected_dirs.append('EKS')
    else:
        dirs = list_directories()
        selected_dirs = get_user_choices(dirs)
    
    main(selected_dirs)