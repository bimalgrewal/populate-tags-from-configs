import yaml
import json
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--configFile', required=True, type=str)
parser.add_argument('--templateFile', required=True, type=str)
parser.add_argument('--outputFile', required=True, type=str)

args = parser.parse_args()
config_file = args.configFile
template_file = args.templateFile
output_file = args.outputFile


# Read the config file
def read_yaml_config(config_file_name):
    try:
        config = open(config_file_name)
        parsed_config = yaml.load(config, Loader=yaml.FullLoader)
        return parsed_config
    except OSError as error:
        print("ERROR: Could not open/read file: ", config_file_name)
        sys.exit()


# Read the template for tags
def read_json_template(template_file_name):
    try:
        template = open(template_file_name)
        empty_template = json.load(template)
        return empty_template
    except OSError:
        print("ERROR: Could not open/read file:", template_file_name)
        sys.exit()


# Merge the config and the template, and output the auto.tfvars.json
def merge_config_template(empty_template, parsed_config, output_file_name):
    tags = {}
    for key, value in empty_template["tags"].items():
        value = parsed_config.get(key)
        if value is None:
            print("ERROR: '%s' is missing from the config" % key)
            return
        tags[key] = value

    output = {'tags': tags}
    with open(output_file_name, 'w') as file:
        file.write(json.dumps(output))

    print("DONE.... %s CREATED." %output_file_name)


def main():
    print("Merging the config and the template...")
    parsed_config = read_yaml_config(config_file)
    empty_template = read_json_template(template_file)
    merge_config_template(empty_template, parsed_config, output_file)


if __name__ == "__main__":
    main()
