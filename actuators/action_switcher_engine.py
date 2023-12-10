import yaml

def read_yaml_file(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data


# read the yaml file.
data = read_yaml_file('action_switcher.yaml')