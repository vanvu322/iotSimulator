import time
import random
import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/temperature"

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Sensor connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

client.on_connect = on_connect

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

while True:
    temperature = round(random.uniform(20.0, 30.0), 2)  # Giả lập dữ liệu nhiệt độ
    client.publish(MQTT_TOPIC, temperature)
    print(f"Sent temperature data: {temperature}")
    time.sleep(15)  # Gửi dữ liệu mỗi 15 giây
