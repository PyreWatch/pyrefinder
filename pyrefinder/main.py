import json
import logging
import os

import paho.mqtt.client as mqtt

from . import db, image, utils

host = "localhost"
port = 1883


def on_connect(client, userdata, flags, rc):
    """On connection, subscribes to the following topics
        - dt/fighter/+ : all fighter devices -> json
        - dt/fighter/+/lwt : all fighter devices last will -> str
        - dt/fighter_alerts : all fighter alerts -> json
        - cmd/fighter/+ : all fighter json responses -> json
    
    Args:
        client (mqtt.Client()): the mqtt client
        userdata (any): private user data added (not used)
        flags: (dict[str]): response flags from the broker
        rc: (int): connection result (0 success, 1 error)

    Returns:
        None: nothing  
    """
    if rc == 0:
        client.subscribe([("dt/fighter/+", 1), ("dt/fighter/+/lwt", 1),
                          ("dt/fighter/+/fire_image", 1),
                          ("dt/fighter/alerts", 2),
                          ("dt/fighter/+/nofire_image", 1)])
    else:
        return


def fighter_status_callback(client, userdata, msg):
    """Callback for listening to fighter statuses: 

    Args:
        client (mqtt.Client()): the mqtt client
        userdata (any): private user data added (not used)
        msg (json): json with lat, lng, and status of fire
    """
    logging.debug(f"Adding status point to fighter_data")
    jsondict = json.loads(msg.payload)
    db.add_fighter_status(msg.topic, jsondict)


def fighter_lwt_callback(client, userdata, msg):
    """Callback for listening to fighter last wills: 

    Args:
        client (mqtt.Client()): the mqtt client
        userdata (any): private user data added (not used)
        msg (str): last will payload: string [Online, Offline]
    """
    client_id = utils.client_from_topic(msg.topic)
    now = image.get_now(spaces=True)
    device_status = str(msg.payload.decode("utf-8"))

    if device_status == "Offline":
        logging.error(
            f"Client {client_id} disconnected from Pyrefinder on {now}.")

    elif device_status == "Online":
        logging.debug(f"Client {client_id} connected to Pyrefinder on {now}.")


def fighter_fire_image_callback(client, userdata, msg):
    """Callback for listening to fighter images:

    Args:
        client (mqtt.Client()): the mqtt client
        userdata (any): private user data added (not used)
        msg (bytes): the byte representation of the image
    """
    im = image.bytes_to_image(msg.payload)
    filepath = image.create_image_filename(msg.topic)
    image.save_image("images/fire", filepath, im)
    db.update_image_path(f"images/fire/{filepath}")


def fighter_nofire_image_callback(client, userdata, msg):
    """Callback for listening to fighter images:

    Args:
        client (mqtt.Client()): the mqtt client
        userdata (any): private user data added (not used)
        msg (bytes): the byte representation of the image
    """
    im = image.bytes_to_image(msg.payload)
    filepath = image.create_image_filename(msg.topic)
    path = image.save_image("images/nofire", filepath, im)

    if path == "NOTSAVED":
        pass

    db.update_image_path(f"images/nofire/{filepath}")


def fighter_alerts_callback(client, userdata, msg):
    """Callback for listening to fighter alerts: 

    Args:
        client (mqtt.Client()): the mqtt client
        userdata (any): private user data added (not used)
        msg (json): json with client id of sender and the alert
    """
    jsondict = json.loads(msg.payload)

    client_id = jsondict['client_id']
    alert = jsondict['alert']

    logging.debug(
        f"Fire detected from fighter {client_id}. Alert infomation: {alert}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()

    client = mqtt.Client()
    client.enable_logger(logger)

    client.on_connect = on_connect

    client.message_callback_add("dt/fighter/+", fighter_status_callback)
    client.message_callback_add("dt/fighter/+/lwt", fighter_lwt_callback)
    client.message_callback_add("dt/fighter/+/fire_image",
                                fighter_fire_image_callback)
    client.message_callback_add("dt/fighter/+/nofire_image",
                                fighter_nofire_image_callback)
    client.message_callback_add("dt/fighter_alerts", fighter_alerts_callback)

    client.connect(host, port)
    client.loop_forever()
