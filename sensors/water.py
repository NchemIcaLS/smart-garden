import time
from grove.gpio import GPIO


class GroveWaterSensor:

    def __init__(self, pin):
        self.pin = water_sensor = GPIO(pin, GPIO.IN)

    @property
    def value(self):
        return self.pin.read()


def main():
    sensor = GroveWaterSensor(5)

    print('Detecting ...')
    while True:
        value = sensor.value
        if sensor.value == 0:
            print("{}, Detected Water.".format(value))
        else:
            print("{}, Dry.".format(value))

        time.sleep(0.5)


if __name__ == '__main__':
    main()
