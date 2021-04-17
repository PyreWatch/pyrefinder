import json
import io
from PIL import Image

import paho.mqtt.publish as publish

if __name__ == "__main__":
    ## SETUP ##

    # creating an image for image sending
    image = Image.open("87205_1.jpg")
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, "PNG")

    # creating a json object for testing alerts
    alert_dict = {"client_id": "bob", "alert": "extra info about the fire"}
    alert = json.dumps(alert_dict)

    # creating a json object for testing statuses
    status_dict = {"status": "FIRE", "latitude": 100, "longitude": 100}
    status = json.dumps(status_dict)

    ## TESTS ##

    # test for status updates where fighter was not in db
    publish.single("dt/fighter/bob", status, client_id="bob")
    publish.single("dt/fighter/tom", status, client_id="tom")

    # test image where file was not detected being sent
    publish.single("dt/fighter/bob/nofire_image",
                   imgByteArr.getvalue(),
                   client_id="bob")

    # test image where fire was detected being sent
    publish.single("dt/fighter/tom/fire_image",
                   imgByteArr.getvalue(),
                   client_id="tom")

    # test if a device disconnects from pyrefinder
    publish.single("dt/fighter/bob/lwt", "Offline", client_id="bob")

    # test if a device disconnects from pyrefinder
    publish.single("dt/fighter/bob/lwt", "Online", client_id="bob")

    # test if an alert is sent:
    publish.single("dt/fighter_alerts", alert, client_id="tom")
