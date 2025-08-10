import os
from flask import Flask, request, jsonify
from datetime import datetime, timezone, timedelta
from pymongo import MongoClient
import statistics
from dotenv import load_dotenv

# Load env
load_dotenv()

app = Flask(__name__)

# Ambil dari environment variable
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["sensor_db"]
collection = db["sensor_data"]

# ===== POST API =====
@app.route("/sensor1", methods=["POST"])
def post_sensor():
    data = request.get_json()
    if not data or "sensor_name" not in data or "temperature" not in data or "humidity" not in data:
        return jsonify({"message": "Invalid data"}), 400

    doc = {
        "sensor_name": data["sensor_name"],
        "temperature": float(data["temperature"]),
        "humidity": float(data["humidity"]),
        "timestamp": datetime.now(timezone.utc)
    }
    collection.insert_one(doc)
    return jsonify({"message": "Data berhasil disimpan"}), 201

# ===== GET All Data =====
@app.route("/sensor1/<sensor_name>/all", methods=["GET"])
def get_all(sensor_name):
    sort_order = request.args.get("sort")
    tz_offset = request.args.get("tz", type=float, default=0)

    cursor = list(collection.find({"sensor_name": sensor_name}, {"_id": 0}))
    for doc in cursor:
        tz_target = timezone(timedelta(hours=tz_offset))
        doc["timestamp"] = doc["timestamp"].astimezone(tz_target).isoformat()

    if sort_order == "lowest":
        cursor.sort(key=lambda x: x["temperature"])
    elif sort_order == "highest":
        cursor.sort(key=lambda x: x["temperature"], reverse=True)

    return jsonify(cursor), 200

# ===== GET Avg Temperature =====
@app.route("/sensor1/<sensor_name>/avg", methods=["GET"])
def get_avg(sensor_name):
    start_date = request.args.get("start")
    end_date = request.args.get("end")

    query = {"sensor_name": sensor_name}
    if start_date and end_date:
        try:
            start_dt = datetime.strptime(start_date, "%d-%m-%Y").replace(tzinfo=timezone.utc)
            end_dt = datetime.strptime(end_date, "%d-%m-%Y").replace(tzinfo=timezone.utc)
            query["timestamp"] = {"$gte": start_dt, "$lte": end_dt}
        except ValueError:
            return jsonify({"message": "Format tanggal harus DD-MM-YYYY"}), 400

    cursor = collection.find(query, {"_id": 0})
    temps = [doc["temperature"] for doc in cursor]

    if not temps:
        return jsonify({"message": "Tidak ada data"}), 404

    avg_temp = statistics.mean(temps)
    return jsonify({"average_temperature": avg_temp}), 200

if __name__ == "__main__":
    app.run(debug=True)
