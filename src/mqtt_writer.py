# https://medium.com/python-point/mqtt-basics-with-python-examples-7c758e605d4
import paho.mqtt.client as mqtt

# TODO: Log error on problems

client = mqtt.Client("EnergyPulseReader")

def connectMQTT(mqttUrl: str):
    print(f"Connecting to MQTT broker in '{mqttUrl}'...")
    client.connect(mqttUrl)
    client.loop_start()

def writeToMQTTAsync(topic: str, payload: str):
    # Send data
    client.publish(topic, payload)

    