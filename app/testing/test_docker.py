import json
import os
import subprocess
import sys
import time
import unittest
import logging

from _pytest.fixtures import pytest_fixture_setup
import numpy as np
import pandas as pd
import pytest
import requests

# in order to add the correct path to the system to import score
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.utils import get_project_root

logger = logging.getLogger("docker_logger")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("pytest.log")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


DATA_DIR = os.path.join(get_project_root(), "data")
IMAGE_NAME = "assignment_4_docker_image"
CONTAINER_NAME = "assignment_4_docker_container"


class TestDockerContainer(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.image_name = IMAGE_NAME
        cls.container_name = CONTAINER_NAME

        # before proceeding we need to ensure that no image or container with
        # the same name exists
        subprocess.run(["docker", "rm", "-f", f"{cls.container_name}"], check=False)
        logger.info(f"Deleted {cls.container_name} if exists.")
        subprocess.run(["docker", "rmi", f"{cls.image_name}"], check=False)
        logger.info(f"Deleted {cls.image_name} if exists.")

        # build the docker image and run the container
        subprocess.run(
            ["docker", "build", "--network=host", "-t", f"{cls.image_name}", "."],
            check=True,
        )
        logger.info(f"Built image {cls.image_name} succesfully.")
        subprocess.run(
            [
                "docker",
                "run",
                "-d",
                "--network=host",
                f"--name={cls.container_name}",
                "-p",
                "5000:5000",
                f"{cls.image_name}",
                # "tail",
                # "-f",
                # "/dev/null",
            ],
            check=True,
        )
        logger.info(f"Ran container {cls.container_name} succesfully.")
        cls.test_dataset = pd.read_csv(os.path.join(DATA_DIR, "test.csv"))
        logger.info("Loaded test dataset succesfully.")
        time.sleep(10)

    def test_docker(self):
        text = self.test_dataset.loc[
            np.random.choice(self.test_dataset.index, 1), "text"
        ]
        data = {"text": text.values[0]}
        url = "http://127.0.0.1:5000/score"
        # Convert the data to JSON format
        json_data = json.dumps(data)
        # Set the headers for the request
        headers = {"Content-Type": "application/json"}
        # Send the POST request
        response = requests.post(url, data=json_data, headers=headers)
        logger.info("Sent request to the app.")
        if response.status_code != 200:
            pytest.fail("Status code is not 200.")

    @classmethod
    def tearDownClass(cls):
        logger.info("Started teardown.")
        subprocess.run(["docker", "stop", cls.container_name], check=True)
        logger.info("Stopped the container.")
        subprocess.run(["docker", "rm", cls.container_name], check=True)
        logger.info("Deleted the container.")
        subprocess.run(["docker", "rmi", cls.image_name], check=True)
        logger.info("Deleted the image.")
