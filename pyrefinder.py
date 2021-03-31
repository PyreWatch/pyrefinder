import os

import paho.mqtt.client as mqtt

host = os.getenv('PF_HOST')
port = os.getenv('PF_PORT')


def on_connect(client, userdata, flags, rc):
    """
    Args:
        client (mqtt.Client()): the mqtt client
        userdata (any): private user data added (not used)
        flags: (dict[str]): response flags from the broker
        rc: (int): connection result (0 success, 1 error)

    Returns:
        Connects client, on connection to the following topics
        - dt/fighter/+ : all fighter devices (expects a json status)
        - dt/fighter/+/lwt : all fighter devices last will (to see if devices disconnect)
        - dt/fighter/alerts : all fighter alerts (if any come in)
        - cmd/fighter/+ : all fighter json responses (command and if it was a success or failure)  
    """
    if rc == 0:
        print("Connected")
        client.subscribe([("dt/fighter/+", 1), ("dt/fighter/+/lwt", 1),
                          ("dt/fighter/alerts", 2), ("cmd/fighter/+", 1)])
    else:
        print("Failed to connect")


def fighter_status_callback(client, userdata, msg):
    """Callback for listening to fighter statuses: 

    Args:
        client (mqtt.Client()): the mqtt client
        userdata (any): private user data added (not used)
        msg (json): json with lat, lng, image, and status of fire
    """
    print(msg.topic + " " + str(msg.payload))


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


def fighter_cmd_res_callback(client, userdata, msg):
    """Callback for listening to fighter responses to commands

    Args:
        client (mqtt.Client()): the mqtt client
        userdata (any): private user data added (not used)
        msg (json): json with the command ran, result, and error message if present
    """    
    print(msg.topic + " " + str(msg.payload))


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect

    client.message_callback_add("dt/fighter/+", fighter_status_callback)
    client.message_callback_add("dt/fighter/+/lwt", fighter_lwt_callback)
    client.message_callback_add("dt/fighter/alerts", fighter_alerts_callback)
    client.message_callback_add("cmd/fighter/+", fighter_cmd_res_callback)

    client.connect(host, port)
    client.loop_forever()
