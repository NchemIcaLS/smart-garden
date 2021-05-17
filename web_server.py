import sqlite3
from datetime import datetime
from sensors import GroveMoistureSensor, GroveHumidityTemperatureSensor, GroveLightSensor, Grove4chRelay
from flask import Flask, render_template, redirect, request

app = Flask(__name__)

relay = Grove4chRelay(0x11)


@app.route("/")
def index():
    now = datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")

    dht = GroveHumidityTemperatureSensor("11", 22)
    SI1145 = GroveLightSensor(0x60)
    A0 = GroveMoistureSensor(0)
    A2 = GroveMoistureSensor(2)
    A4 = GroveMoistureSensor(4)
    A6 = GroveMoistureSensor(6)

    humidity, temperature = dht.read()
    light_visible = SI1145.ReadVisible
    light_uv = SI1145.ReadUV / 100
    light_ir = SI1145.ReadIR
    moisture = [A0.moisture, A2.moisture, A4.moisture, A6.moisture]

    con = sqlite3.connect(
        'database.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
    cur = con.cursor()

    def fetch_data(sensor_id):
        cur.execute(
            f"SELECT timestamp, value FROM data WHERE sensor_id = {sensor_id} ORDER BY timestamp")
        res = cur.fetchall()

        timestamps = []
        values = []
        for timestamp, value in res:
            timestamps.append(str(timestamp)[:19])
            values.append(value)

        return timestamps, values

    templateData = {
        'time': timeString,
        'humidity': humidity,
        'temperature': temperature,
        'light_visible': light_visible,
        'light_uv': light_uv,
        'light_ir': light_ir,
        'moisture': moisture,
        'tempertemperature': temperature,
        'data_timestamps': fetch_data(0)[0],
        'data_temperature': fetch_data(0)[1],
        'data_humidity': fetch_data(1)[1],
        'data_light_visible': fetch_data(2)[1],
        'data_light_uv': fetch_data(3)[1],
        'data_light_ir': fetch_data(4)[1],
        'data_moisture_1': fetch_data(5)[1],
        'data_moisture_2': fetch_data(6)[1],
        'data_moisture_3': fetch_data(7)[1],
        'data_moisture_4': fetch_data(8)[1],
    }
    return render_template('index.html', **templateData)


@app.route("/water_on")
def water_on_all():
    relay.turn_on_all()
    return redirect('/')


@app.route("/water_on/<int:channel>")
def water_on(channel):
    relay.turn_on(channel)
    return redirect('/')


@app.route("/water_off")
def water_off_all():
    relay.turn_off_all()
    return redirect('/')


@app.route("/water_off/<int:channel>")
def water_off(channel):
    relay.turn_off(channel)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
