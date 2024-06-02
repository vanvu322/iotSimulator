import time
import random
import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_SENSOR_TOPIC = "sensor/temperature"
MQTT_ACTUATOR_TOPIC = "actuator/control"

client = mqtt.Client()

current_interval = 15  # Default interval
sending_data = True    # Default state to send data
aircon_enabled = False # Default state of air conditioner
aircon_temp_range = (22.0, 24.0)  # Default temperature range for aircon

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Sensor connected to MQTT Broker!")
        client.subscribe(MQTT_ACTUATOR_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    global current_interval, sending_data, aircon_enabled, aircon_temp_range
    command = msg.payload.decode()
    print(f"Received control command: {command}")
    try:
        if command.startswith("interval:"):
            interval = int(command.split(":")[1])
            current_interval = interval
            print(f"Updated interval to: {current_interval} seconds")
        elif command == "start":
            sending_data = True
            print("Started sending data")
        elif command == "stop":
            sending_data = False
            print("Stopped sending data")
        elif command.startswith("aircon:"):
            state = command.split(":")[1]
            if state == "on":
                aircon_enabled = True
                print("Air conditioner turned on")
            elif state == "off":
                aircon_enabled = False
                print("Air conditioner turned off")
        elif command.startswith("aircon_temp_range:"):
            temp_range = command.split(":")[1]
            min_temp, max_temp = map(float, temp_range.split(","))
            aircon_temp_range = (min_temp, max_temp)
            print(f"Updated air conditioner temperature range to: {aircon_temp_range}")
    except Exception as e:
        print(f"Failed to process command: {e}")

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

while True:
    if sending_data:
        if aircon_enabled:
            temperature = round(random.uniform(aircon_temp_range[0], aircon_temp_range[1]), 2)
        else:
            temperature = round(random.uniform(20.0, 30.0), 2)
        client.publish(MQTT_SENSOR_TOPIC, temperature)
        print(f"Sent temperature data: {temperature}")
    time.sleep(current_interval)
