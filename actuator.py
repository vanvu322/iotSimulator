import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_ACTUATOR_TOPIC = "actuator/control"

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Actuator connected to MQTT Broker!")
        client.subscribe(MQTT_ACTUATOR_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    command = msg.payload.decode()
    print(f"Received command for actuator: {command}")
    # Thực hiện hành động tương ứng với lệnh nhận được
    # Ví dụ: bật/tắt thiết bị, thay đổi trạng thái, v.v.

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
