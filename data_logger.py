import time
import datetime
import sqlite3
import numpy as np

from sensors import GroveMoistureSensor, GroveHumidityTemperatureSensor, GroveLightSensor

con = sqlite3.connect('database.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
cur = con.cursor()

dht = GroveHumidityTemperatureSensor("11", 22)
SI1145 = GroveLightSensor(0x60)
A0 = GroveMoistureSensor(0)
A2 = GroveMoistureSensor(2)
A4 = GroveMoistureSensor(4)
A6 = GroveMoistureSensor(6)

num_sensors = 9
interval = 3600  # 1 hour
n = 20  # Repeat measurement 20 times

data = np.zeros((num_sensors, n), dtype=int)
wait = interval / n

while True:
    time.sleep(interval - time.time() % interval)

    timestamp = datetime.datetime.now()

    for i in range(n):
        if i > 0:
            time.sleep(wait)
        data[1][i], data[0][i] = dht.read()
        data[2][i] = SI1145.ReadVisible
        data[3][i] = SI1145.ReadUV
        data[4][i] = SI1145.ReadIR
        data[5][i] = A0.moisture
        data[6][i] = A2.moisture
        data[7][i] = A4.moisture
        data[8][i] = A6.moisture

    values = np.mean(data, axis=1, dtype=int)

    for sensor_id, value in enumerate(values):
        query = f"INSERT INTO data VALUES (NULL, '{timestamp}', '{sensor_id}', '{value}')"
        cur.execute(query)

    con.commit()
