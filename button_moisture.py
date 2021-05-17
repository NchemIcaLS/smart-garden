import time
from sensors import GroveButton, Grove4chRelay, GroveMoistureSensor

def main():
    button = GroveButton(12)
    relay = Grove4chRelay(0x11)

    plants = [
        {
            "name": "basil-1",
            "sensor": GroveMoistureSensor(4),
            "channel": 1
        },
        {
            "name": "basil-2",
            "sensor": GroveMoistureSensor(6),
            "channel": 4
        },
        {
            "name": "oregano",
            "sensor": GroveMoistureSensor(2),
            "channel": 3
        },
        {
            "name": "tomato",
            "sensor": GroveMoistureSensor(0),
            "channel": 2
        },
    ]

    def on_press():
        for plant in plants:
            moisture = plant.get("sensor").moisture
            if moisture > 1600:
                relay.turn_on(plant.get("channel"))
                while moisture > 1600:
                    moisture = plant.get("sensor").moisture
                    time.sleep(1)
                relay.turn_off(plant.get("channel"))
    button.on_press = on_press

    def on_release():
        relay.turn_off_all()
    button.on_release = on_release

    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
