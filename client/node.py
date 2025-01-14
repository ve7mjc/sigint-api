from common.schemas.node import (
    NodeConfig,
    NodeRegistration,
    NodeRegisterRequest,
    NodeRegisterResponse
)
from literals import API_URL_BASE

import asyncio
import json
from pathlib import Path
import logging
from datetime import datetime
import argparse
from typing import Optional

import aiohttp
import yaml


# logging.basicConfig()
logger = logging.getLogger()
# log.setLevel(logging.DEBUG)
# logging.getLogger('asyncio').setLevel(logging.INFO)  # shush

# Custom JSON serializer to handle datetime
def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Convert to ISO 8601 format with timezone
    raise TypeError(f"Type {type(obj)} not serializable")

# Create a custom dumps function for aiohttp
def custom_json_dumps(data):
    return json.dumps(data, default=custom_serializer)


# Define timeouts
timeout = aiohttp.ClientTimeout(
    total=10,        # Total timeout for the request
    connect=2,       # Timeout for establishing a connection
    sock_connect=2,  # Timeout for connecting to the socket
    sock_read=5      # Timeout for reading from the socket
)


async def register_node(node: NodeConfig) -> NodeRegisterResponse:

    url = API_URL_BASE + "nodes/register"

    request = NodeRegisterRequest(
        name=node.name,
        fixed_location=node.fixed_location,
        antenna_height=node.antenna_height
    )

    json_payload = request.model_dump()

    try:
        async with aiohttp.ClientSession(
                timeout=timeout, json_serialize=custom_json_dumps
            ) as session:
            async with session.post(url, json=json_payload) as response:

                if response.status == 200:
                    response_data = await response.json()
                    response = NodeRegisterResponse(**response_data)
                    return response
                else:
                    logger.error(f"Request failed with status {response.status}: {await response.text()}")

    except Exception as e:
        raise Exception(f"Exception occurred: {e}")


async def get_node_registration(node: NodeConfig) -> NodeRegistration:
    response = await register_node(node)
    if response.new_registration:
        logger.info(f"registered node '{response.name}' with id = '{response.id}'")
    if response.registration is None:
        raise Exception("unable to register node or get registration!")
    return response.registration


async def load_node_config(file_path: Optional[Path] = None) -> NodeConfig:

    if file_path is None:

        # check commandline arguments
        parser = argparse.ArgumentParser(description="Load and process a YAML file.")
        parser.add_argument(
            "yaml_file", type=Path, help="Path to the node config YAML file"
        )
        args = parser.parse_args()
        file_path = args.yaml_file

    try:

        if not file_path.exists():
            raise FileNotFoundError(file_path)

        with open(file_path, "r", encoding="ascii") as file:
            yaml_data = yaml.safe_load(file)
            node_config = NodeConfig.model_validate(yaml_data)
            return node_config

    except Exception as e:
        print(f"Exception loading node config: {e}")



