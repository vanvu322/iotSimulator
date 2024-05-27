from flask import Flask, render_template, jsonify
from flask_mqtt import Mqtt
import json
import os

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'localhost'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_TOPIC'] = 'sensor/temperature'

mqtt = Mqtt(app)

# Đường dẫn tới tệp JSON
JSON_FILE_PATH = "temperature_data.json"

# Hàm xử lý sự kiện kết nối đến MQTT broker
@mqtt.on_connect()
def handle_mqtt_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        mqtt.subscribe(app.config['MQTT_TOPIC'])
    else:
        print(f"Failed to connect to MQTT Broker, return code {rc}")

# Hàm xử lý sự kiện nhận tin nhắn từ MQTT broker
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    try:
        data = float(message.payload.decode())
        print(f"Received MQTT message: {data}")  # Hiển thị dữ liệu nhận được từ sensor
        # Đọc dữ liệu từ file JSON nếu đã tồn tại
        try:
            with open(JSON_FILE_PATH, "r") as json_file:
                temperature_data = json.load(json_file)
        except FileNotFoundError:
            temperature_data = []
        # Thêm dữ liệu mới vào danh sách
        temperature_data.append({"temperature": data})
        # Lưu lại dữ liệu vào file JSON
        with open(JSON_FILE_PATH, "w") as json_file:
            json.dump(temperature_data, json_file)
        print("Saved temperature data to JSON file")
    except Exception as e:
        print(f"Error: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    try:
        # Kiểm tra xem tệp JSON có tồn tại không
        if not os.path.exists(JSON_FILE_PATH):
            # Nếu không tồn tại, khởi tạo một danh sách trống
            with open(JSON_FILE_PATH, "w") as json_file:
                json.dump([], json_file)
            print(f"Created new JSON file: {JSON_FILE_PATH}")
        
        # Đọc dữ liệu từ tệp JSON
        with open(JSON_FILE_PATH, "r") as json_file:
            temperature_data = json.load(json_file)
        return jsonify(temperature_data), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to retrieve data"}), 500
if __name__ == '__main__':
    app.run(debug=True)