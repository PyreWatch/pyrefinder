import os

from PIL import Image
from pyrefinder import image


def test_create_image_filename():
    topic = "dt/fighter/bob/nofire"

    time = image.get_now(spaces=False)

    assert image.create_image_filename(topic) == f"bob_{time}.jpg"


def test_save_image():
    file = Image.open("87205_1.jpg")
    path = "images/fire"
    filename = "tester.jpg"

    image.save_image(path, filename, file)

    assert os.path.isfile(f"{path}/{filename}")