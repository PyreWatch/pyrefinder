import paho.mqtt.client as mqtt
import logging


def on_connect(client, userdata, flags, rc):
    '''
    Takes in connection info and subscribes to the following topics:
    - dt/fighter/+ : all fighter devices (expects a json status)
    - dt/fighter/+/lwt : all fighter devices last will (to see if devices disconnect)
    - dt/fighter/alerts : all fighter alerts (if any come in)
    - cmd/fighter/+ : all fighter json responses (command and if it was a success or failure)  
    '''
    if rc == 0:
        print("Connected")
        client.subscribe([("dt/fighter/+", 1), ("dt/fighter/+/lwt", 1),
                          ("dt/fighter/alerts", 2), ("cmd/fighter/+", 1)])
    else:
        print("Failed to connect")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.loop_forever()