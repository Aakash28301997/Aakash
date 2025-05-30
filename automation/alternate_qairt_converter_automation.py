
import os
import yaml
import json
import argparse
from loguru import logger
from subprocess import Popen, PIPE

class QairtConverterAutomation:
    def __init__(self, config_path, output_json, execute=False):
        self.config_path = config_path
        self.output_json = output_json
        self.execute_flag = execute
        self.base_cmd = ["qairt-converter"]
        self.commands = []

    def load_yaml_config(self):
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load YAML config: {e}")
            raise

    def build_commands(self, config):
        input_network = config.get("input_network")
        if not input_network:
            raise ValueError("Missing required 'input_network' in config")

        def append_command(arg_list):
            cmd = self.base_cmd.copy()
            cmd += arg_list
            self.commands.append(cmd)

        if "source_model_input_shape" in config:
            for input_name, dims in config["source_model_input_shape"].items():
                append_command(["--input_network", input_network,
                                "--source_model_input_shape", input_name] + list(map(str, dims)))

        if "out_tensor_name" in config:
            for out_name in config["out_tensor_name"]:
                append_command(["--input_network", input_network,
                                "--out_tensor_name", out_name])

        if "source_model_input_datatype" in config:
            for name, dtype in config["source_model_input_datatype"].items():
                append_command(["--input_network", input_network,
                                "--source_model_input_datatype", name, dtype])

        if "source_model_input_layout" in config:
            for name, layout in config["source_model_input_layout"].items():
                append_command(["--input_network", input_network,
                                "--source_model_input_layout", name, layout])

    def save_commands_to_json(self):
        try:
            with open(self.output_json, 'w') as f:
                json.dump([" ".join(cmd) for cmd in self.commands], f, indent=4)
            logger.info(f"Commands saved to {self.output_json}")
        except Exception as e:
            logger.error(f"Failed to write output JSON: {e}")
            raise

    def execute_commands(self):
        for cmd in self.commands:
            logger.info(f"Executing: {' '.join(cmd)}")
            process = Popen(cmd, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            logger.info(stdout.decode())
            if stderr:
                logger.error(stderr.decode())

    def run(self):
        config = self.load_yaml_config()
        self.build_commands(config)
        self.save_commands_to_json()
        if self.execute_flag:
            self.execute_commands()

def main():
    parser = argparse.ArgumentParser(description="Automate qairt-converter with class-based structure")
    parser.add_argument("--config", required=True, help="Path to YAML config file")
    parser.add_argument("--output_json", required=True, help="Path to save generated command JSON")
    parser.add_argument("--execute", action="store_true", help="Flag to execute the generated commands")
    args = parser.parse_args()

    tool = QairtConverterAutomation(args.config, args.output_json, args.execute)
    tool.run()

if __name__ == "__main__":
    main()
