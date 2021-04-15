import io
import os
import logging
import datetime
from pyrefinder import db, utils

from PIL import Image

# Defines the base directory for the project; utilized for image storage
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def get_now():
    """Get the current time for using to save the file uniquely

    Returns:
        [datetime]: returns the current time 
    """
    return datetime.datetime.now().strftime("%b%d%Y%H:%M:%S")


def bytes_to_image(bytes):
    """Convert byte array from mqtt message into an image

    Args:
        bytes (bytes): the byte array that is the image from fighter

    Returns:
        [Image]: the image from fighter
    """
    return Image.open(io.BytesIO(bytes))


def create_image_filename(topic):
    """ Creates an image filename using the current time and the client id

    Args:
        topic (str): the topic where the the message was sent to; utilized to get the client id

    Returns:
        [str]: filename including extension, i.e. bob_Apr15202100:21:53.jpg
    """
    time = get_now()
    client_id = utils.client_from_topic(topic)

    return f"{client_id}_{time}.jpg"


def save_image(path, filename, image):
    """Save image in to the proper path based off fire status

    Args:
        path (str): the string path for where the images should be saved, i.e images/fire or images/nofire
        filename (str): the filename for where the image will be saved
        image (Image): the image from fighter

    Return:
        [str]: returns path to that file including the file name: i.e. images/nofire/image.jpg
    """
    if not os.path.exists(f"{BASE_DIR}/{path}"):
        try:
            os.makedirs(f"{BASE_DIR}/{path}")
        except OSError as e:
            logging.error(
                f"Error creating folder {BASE_DIR}/{path} with the following error: %d",
                e)

    image.save(f"{path}/{filename}")

    return f"{BASE_DIR}/{path}/{filename}"
