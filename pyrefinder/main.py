import json
import logging
import os

import paho.mqtt.client as mqtt

from . import db

host = os.getenv('PF_HOST')
port = 1883


def on_connect(client, userdata, flags, rc):
    """On connection, subscribes to the following topics
        - dt/fighter/+ : all fighter devices -> json
        - dt/fighter/+/lwt : all fighter devices last will -> str
        - dt/fighter/alerts : all fighter alerts -> json
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
                          ("dt/fighter/alerts", 2), ("cmd/fighter/+", 1)])
    else:
        return


def fighter_status_callback(client, userdata, msg):
    """Callback for listening to fighter statuses: 

    Args:
        client (mqtt.Client()): the mqtt client
        userdata (any): private user data added (not used)
        msg (json): json with lat, lng, image, and status of fire
    """
    logging.debug(f"Adding status point {msg.payload} to fighter_data")
    jsondict = json.loads(msg.payload)
    db.add_fighter_status(msg.topic, jsondict)


def fighter_lwt_callback(client, userdata, msg):
    """Callback for listening to fighter last wills: 

    Args:
        client (mqtt.Client()): the mqtt client
        userdata (any): private user data added (not used)
        msg ((str): last will payload: string [Online, Offline]
    """
    print(msg.topic + " " + str(msg.payload))


def fighter_alerts_callback(client, userdata, msg):
    """Callback for listening to fighter alerts: 

    Args:
        client (mqtt.Client()): the mqtt client
        userdata (any): private user data added (not used)
        msg (json): json with client id of sender and the alert
    """
    print(msg.topic + " " + str(msg.payload))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger()

    client = mqtt.Client()
    client.enable_logger(logger)

    client.on_connect = on_connect

    client.message_callback_add("dt/fighter/+", fighter_status_callback)
    client.message_callback_add("dt/fighter/+/lwt", fighter_lwt_callback)
    client.message_callback_add("dt/fighter/alerts", fighter_alerts_callback)

    client.connect(host, port)
    client.loop_forever()
