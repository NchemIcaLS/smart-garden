import time
import datetime
import sqlite3
from sensors import GroveMoistureSensor, GroveHumidityTemperatureSensor, GroveLightSensor

con = sqlite3.connect('database.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
cur = con.cursor()


dht = GroveHumidityTemperatureSensor("11", 22)
SI1145 = GroveLightSensor(0x60)
A0 = GroveMoistureSensor(0)
A2 = GroveMoistureSensor(2)
A4 = GroveMoistureSensor(4)
A6 = GroveMoistureSensor(6)

interval = 900  # 15 minutes
n = 15 # Repeat measurement 15 times

while True:
    time.sleep(interval - time.time() % interval)

    timestamp = datetime.datetime.now()

    temperature = 0
    humidity = 0
    light_visible = 0
    light_uv = 0
    light_ir = 0
    moisture_1 = 0
    moisture_2 = 0
    moisture_3 = 0
    moisture_4 = 0

    for i in range(n):
        h, t = dht.read()
        temperature += t
        humidity += h
        light_visible += SI1145.ReadVisible
        light_uv += SI1145.ReadUV / 100
        light_ir += SI1145.ReadIR
        moisture_1 += A0.moisture
        moisture_2 += A2.moisture
        moisture_3 += A4.moisture
        moisture_4 += A6.moisture
        time.sleep(4)

    temperature = round(temperature / n)
    humidity = round(humidity / n)
    light_visible = round(light_visible / n)
    light_uv = round(light_uv / n)
    light_ir = round(light_ir / n)
    moisture_1 = round(moisture_1 / n)
    moisture_2 = round(moisture_2 / n)
    moisture_3 = round(moisture_3 / n)
    moisture_4 = round(moisture_4 / n)

    # print(f"Temperature: {temperature}, Humidity: {humidity}, Light: {light_visible}, UV: {light_uv}, IR: {light_ir}, Moisture: {(moisture_1, moisture_2, moisture_3, moisture_4)}")

    readings = [
        temperature,
        humidity,
        light_visible,
        light_uv,
        light_ir,
        moisture_1,
        moisture_2,
        moisture_3,
        moisture_4,
    ]

    for sensor_id, value in enumerate(readings):
        query = f"INSERT INTO data VALUES (NULL, '{timestamp}', '{sensor_id}', '{value}')"
        cur.execute(query)

    con.commit()
