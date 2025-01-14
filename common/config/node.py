from common.schemas.node import NodeConfig

import yaml

from pathlib import Path


# def load_node_config(file_path: Path) -> NodeConfig:

#     """Loads a YAML file and returns its contents."""
#     if not file_path.exists():
#         raise FileNotFoundError(f"The file '{file_path}' does not exist.")

#     if not file_path.suffix in {".yaml", ".yml"}:
#         raise ValueError(f"The file '{file_path}' does not have a valid YAML extension.")

#     with open(file_path, "r") as file:
#         if not file_path.exists():
#             raise FileNotFoundError(file_path)

#         yaml_data = yaml.safe_load(file)
#         node_config = NodeConfig.parse_obj(yaml_data)

#         return node_config
