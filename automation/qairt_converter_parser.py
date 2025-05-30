
import argparse
import subprocess
import yaml
import json
from collections import OrderedDict

def load_yaml_config(yaml_path):
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)

def build_qairt_converter_command(config):
    base_cmd = ["qairt-converter"]
    input_network = config.get("input_network")

    if not input_network:
        raise ValueError("Missing required 'input_network' in YAML config")

    command_list = []

    # 1. --source_model_input_shape connection
    if "source_model_input_shape" in config:
        for input_name, dims in config["source_model_input_shape"].items():
            cmd = base_cmd.copy()
            cmd += ["--input_network", input_network]
            cmd += ["--source_model_input_shape", input_name] + list(map(str, dims))
            command_list.append(cmd)

    # 2. --out_tensor_name connection
    if "out_tensor_name" in config:
        for out_name in config["out_tensor_name"]:
            cmd = base_cmd.copy()
            cmd += ["--input_network", input_network]
            cmd += ["--out_tensor_name", out_name]
            command_list.append(cmd)

    # 3. --source_model_input_datatype connection
    if "source_model_input_datatype" in config:
        for input_name, dtype in config["source_model_input_datatype"].items():
            cmd = base_cmd.copy()
            cmd += ["--input_network", input_network]
            cmd += ["--source_model_input_datatype", input_name, dtype]
            command_list.append(cmd)

    # 4. --source_model_input_layout connection
    if "source_model_input_layout" in config:
        for input_name, layout in config["source_model_input_layout"].items():
            cmd = base_cmd.copy()
            cmd += ["--input_network", input_network]
            cmd += ["--source_model_input_layout", input_name, layout]
            command_list.append(cmd)

    return command_list

def save_commands_to_json(commands, json_path):
    with open(json_path, 'w') as f:
        json.dump(commands, f, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Generate qairt-converter commands")
    parser.add_argument("--config", required=True, help="Path to YAML config file")
    parser.add_argument("--output_json", required=True, help="Path to output JSON file")
    parser.add_argument("--execute", action="store_true", help="Execute the generated commands")
    args = parser.parse_args()

    config = load_yaml_config(args.config)
    commands = build_qairt_converter_command(config)

    command_strings = [" ".join(cmd) for cmd in commands]
    save_commands_to_json(command_strings, args.output_json)

    print("Generated Commands:")
    for cmd in command_strings:
        print(cmd)

    if args.execute:
        for cmd in commands:
            subprocess.run(cmd)

if __name__ == "__main__":
    main()
