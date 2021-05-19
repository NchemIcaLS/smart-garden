import sqlite3
import time
import threading
from datetime import datetime
from sensors import GroveMoistureSensor, GroveHumidityTemperatureSensor, GroveLightSensor, GroveButton, Grove4chRelay
from flask import Flask, render_template, redirect

app = Flask(__name__)

# Define moisture sensor and channel pairings
# (name, channel, moisture_sensor, moisture_level)
# sorted by moisture sensor
plants = [
    ("tomato",  2, 0, 1400),
    ("oregano", 3, 1, 1700),
    ("basil-1", 1, 2, 1550),
    ("basil-2", 4, 3, 1550),
]

# Sensors
dht = GroveHumidityTemperatureSensor("11", 22)
SI1145 = GroveLightSensor(0x60)
moisture_sensors = [GroveMoistureSensor(plant[2]*2) for plant in plants]

# Relay
relay = Grove4chRelay(0x11)

###
# Button
###


def button():
    button = GroveButton(12)

    def on_press():
        relay.turn_on_all()

    def on_release():
        relay.turn_off_all()

    button.on_press = on_press
    button.on_release = on_release

###
# Automatic watering

# 0 = none
# 1 = time based
# 2 = moisture sensors


strategy = 0
strategy_changed = threading.Event()


def automatic():
    while True:
        if strategy is 0:
            pass
        elif strategy is 1:
            now = datetime.now()
            # Water for 5 seconds every other day at 6 AM
            if now.hour is 6 and now.day % 2 is 0:
                relay.turn_on_all()
                time.sleep(5)
                relay.turn_off_all()
        elif strategy is 2:
            for plant in plants:
                channel = plant[1]
                sensor = moisture_sensors[plant[2]]
                moisture_level = plant[3]
                # Check if moisture level is greater than desired + buffer
                if sensor.moisture > moisture_level + 100:
                    relay.turn_on(channel)
                    while sensor.moisture > moisture_level:
                        time.sleep(1)
                    relay.turn_off(channel)
        relay.turn_off_all()
        strategy_changed.wait(3600)
        strategy_changed.clear()


###

###
# Database
###


con = sqlite3.connect(
    'database.sqlite', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
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


###
# Routes
###


@app.route("/")
def index():
    global plants, relay, strategy

    now = datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")

    humidity, temperature = dht.read()
    light_visible = SI1145.ReadVisible
    light_uv = SI1145.ReadUV / 100
    light_ir = SI1145.ReadIR
    moisture = [sensor.moisture for sensor in moisture_sensors]

    templateData = {
        'time': timeString,
        'plants': plants,
        'relay_state': relay.get_state(),
        'strategy': strategy,
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
        'data_light_uv': [x / 100 for x in fetch_data(3)[1]],
        'data_light_ir': fetch_data(4)[1],
        'data_moisture_1': fetch_data(5)[1],
        'data_moisture_2': fetch_data(6)[1],
        'data_moisture_3': fetch_data(7)[1],
        'data_moisture_4': fetch_data(8)[1],
    }
    return render_template('index.html', **templateData)


@app.route("/channel_on/<int:channel>")
def channel_on(channel):
    global relay

    if channel is 0:
        relay.turn_on_all()
    elif channel in [1, 2, 3, 4]:
        relay.turn_on(channel)
    else:
        pass
    return redirect('/')


@app.route("/channel_off/<int:channel>")
def channel_off(channel):
    global relay

    if channel is 0:
        relay.turn_off_all()
    elif channel in [1, 2, 3, 4]:
        relay.turn_off(channel)
    else:
        pass
    return redirect('/')


@app.route("/set_strategy/<int:strategy_id>")
def set_strategy(strategy_id):
    global strategy, strategy_changed

    strategy = strategy_id
    strategy_changed.set()
    return redirect('/')


if __name__ == '__main__':
    threading.Thread(name='button', target=button).start()
    threading.Thread(name='automatic', target=automatic).start()
    app.run(debug=True, port=80, host='0.0.0.0')
