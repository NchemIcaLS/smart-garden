import time
from grove.adc import ADC

class GroveMoistureSensor:
    '''
    Grove Moisture Sensor class

    Args:
        pin(int): number of analog pin/channel the sensor connected.
    '''

    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def moisture(self):
        '''
        Get the moisture strength value/voltage

        Returns:
            (int): voltage, in mV
        '''
        value = self.adc.read_voltage(self.channel)
        return value


def main():
    for pin in [0, 2, 4, 6]:
        sensor = GroveMoistureSensor(pin)

        # print('Detecting moisture...')
        # while True:
        m = sensor.moisture
        if m < 1300:
            result = 'Water'
        elif 1300 <= m and m < 1400:
            result = 'Wet'
        elif 1400 <= m and m < 1600:
            result = 'Damp'
        elif 1600 <= m and m < 1900:
            result = 'Moist'
        else:
            result = 'Dry'
        print('Moisture value: {0}, {1}'.format(m, result))
            # time.sleep(1)


if __name__ == '__main__':
    main()
