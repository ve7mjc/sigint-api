from common.schemas.intercept import (
    InterceptCreateRequest,
    InterceptCreateResponse,
    Intercept
)
from common.schemas.node import (
    Node, NodeConfig,
    NodeRegistration, NodeRegisterRequest, NodeRegisterResponse
)
from node import (
    load_node_config,
    get_node_registration
)
from literals import API_URL_BASE


import asyncio
import json
from pathlib import Path
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
import wave
import argparse
from typing import Optional

import aiohttp


datafile = "/opt/data/radio_channels/sh-145350_20250103T190330.wav"
datetime_str = "20250103T190330"

naive_datetime = datetime.strptime(datetime_str, "%Y%m%dT%H%M%S")
time_start = naive_datetime.replace(tzinfo=ZoneInfo("America/Vancouver"))

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)
logging.getLogger('asyncio').setLevel(logging.INFO)


def get_wave_duration(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        n_frames = wav_file.getnframes()
        frame_rate = wav_file.getframerate()
        duration = n_frames / float(frame_rate)
        return duration

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



async def publish_intercept(registration: NodeRegistration,
                            node_config: NodeConfig,
                            intercept: InterceptCreateRequest) -> InterceptCreateResponse:

    url = API_URL_BASE + "intercept/"

    request = InterceptCreateRequest(
        node_id=registration.id,
        frequency_center=intercept.frequency_center,
        time_start=intercept.time_start,
        duration=intercept.duration
    )

    # model to dict
    json_payload = request.model_dump()

    try:
        async with aiohttp.ClientSession(
                timeout=timeout, json_serialize=custom_json_dumps
            ) as session:
            async with session.post(url, json=json_payload) as response:

                if response.status == 200:
                    response_data = await response.json()
                    response = InterceptCreateResponse(**response_data)
                    log.debug("Response received:", response)
                else:
                    log.error(f"Request failed with status {response.status}: {await response.text()}")

    except Exception as e:
        raise Exception(f"Exception occurred: {e}")

"""
async def upload_file(url: str, file_path: Path):

    log.debug(f"using url: {url}")

    # Uploads a binary file with accompanying JSON metadata to the given URL.
    if not Path(file_path).is_file():
        print(f"File {file_path} not found!")
        return

    try:
        async with aiohttp.ClientSession() as session:

            # Add the file
            with open(file_path, 'rb') as file:

                form = aiohttp.FormData()

                # Add JSON payload as a string
                form.add_field(
                    "intercept",
                    json.dumps(asdict(request), default=custom_serializer),
                    content_type="application/json"
                )

                form.add_field(
                    'file',
                    file,
                    filename=file_path,
                    content_type='audio/wav'
                )

                # Send the request
                async with session.post(API_URL, data=form) as response:
                    print(await response.text())

    except Exception as e:
        print(f"An error occurred: {e}")
"""



async def do_intercept(node: NodeRegistration):

    request = InterceptCreateRequest(
        node_name=node.name,
        frequency_center=145.430,
        time_start=time_start,
        duration=get_wave_duration(datafile)
    )

    intercept = Intercept(
        frequency_center=144.725,
        time_start=time_start,
        duration=get_wave_duration(datafile)
    )

    response = await publish_intercept(node, intercept)
    print(response)


async def main():

    try:
        node_config = await load_node_config()
    except Exception as e:
        print(f"Exception loading node config: {e}")

    log.debug(f"loaded node config for node name = : {node_config.name}")

    # get registration
    registration = await get_node_registration(node_config)

    print(registration)

    # publish intercept event
    # intercept = await do_intercept(node_config)

    # upload media



if __name__ == "__main__":
    asyncio.run(main())
