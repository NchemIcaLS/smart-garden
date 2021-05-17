import time
import seeed_dht


def main():

    # for DHT11
    # Plugged into pin 22
    sensor = seeed_dht.DHT("11", 22)

    while True:
        humi, temp = sensor.read()
        if not humi is None:
            print(
                'DHT{0}, humidity {1:.1f}%, temperature {2:.1f}*'.format(sensor.dht_type, humi, temp))
        else:
            print('DHT{0}, humidity & temperature: {1}'.format(
                sensor.dht_type, temp))
        time.sleep(1)


if __name__ == '__main__':
    main()
