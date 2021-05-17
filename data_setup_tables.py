import sqlite3

con = sqlite3.connect('database.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
cur = con.cursor()

cur.execute('DROP TABLE IF EXISTS sensor')
cur.execute('''
CREATE TABLE sensor (
    id INTEGER PRIMARY KEY,
    name TEXT
)''')
cur.execute('''
INSERT INTO sensor
VALUES ('0','temperature'),
    ('1','humidity'),
    ('2','light-visible'),
    ('3','light-uv'),
    ('4','light-ir'),
    ('5','moisture-1'),
    ('6','moisture-2'),
    ('7','moisture-3'),
    ('8','moisture-4')
''')
con.commit()

cur.execute('DROP TABLE IF EXISTS data')
cur.execute('''
CREATE TABLE data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP,
    sensor_id INTEGER,
    value INTEGER,
    FOREIGN KEY(sensor_id) REFERENCES sensor(id)
)''')
con.commit()