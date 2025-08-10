from datetime import datetime
from flask import Flask, request, jsonify


app = Flask(__name__)

sensor_data_list = []

@app.route("/sensor/data", methods=["POST"])
def post_sensor():
    data = request.get_json()

    if not data or "temperature" not in data or "humidity" not in data:
        return jsonify({
            "message": "Invalid data"
        }),400
    
    timestamp = data.get("timestamp", datetime.now().isoformat())

    sensor_data_list.append({
        "temperature": data["temperature"],
        "humidity": data["humidity"],
        "timestamp": timestamp
    })

    return jsonify({"message": "Data berhasil disimpan"}), 201

@app.route("/sensor/data", methods=["GET"])
def get_sensors():
    return jsonify({
        "message": "Data list berhasil didapat",
        "data": sensor_data_list
    }), 200


if __name__ == "__main__":
    app.run(debug=True)