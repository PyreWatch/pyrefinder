import io
import os
import logging

from PIL import Image


def bytes_to_image(path, bytes):
    """Convert byte array from mqtt message into an image and save the image in to the proper path

    Args:
        path (str): the string path for where the images should be saved, i.e images/fire or images/nofire
        bytes (bytes): the byte array that is the image from fighter
    """
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    image = Image.open(io.BytesIO(bytes))

    if not os.path.exists(f"{BASE_DIR}/{path}"):
        try:
            os.makedirs(f"{BASE_DIR}/{path}")
            image.save(f"{path}/returned.jpg")
        except OSError as e:
            logging.error(
                f"Error creating folder {BASE_DIR}/{path} with the following error ",
                e)