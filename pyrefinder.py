import paho.mqtt.client as mqtt
import logging


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected")
        client.subscribe("$SYS/#")
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