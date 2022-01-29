# https://medium.com/python-point/mqtt-basics-with-python-examples-7c758e605d4
import paho.mqtt.client as mqtt

client = mqtt.Client("EnergyPulseReader")

def writeToMQTTAsync(mqttUrl: str, topic: str, payload: str):
    # Connect if necessary
    # TODO: Why does this connect on every write?
    if (not client.is_connected()):
        print(f"Connecting to MQTT broker in '{mqttUrl}'...")
        print(f"Connection result: {client.connect(mqttUrl)}")
    # Send data
    print(f"Sending result: {client.publish(topic, payload)}")

    