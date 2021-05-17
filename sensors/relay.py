from grove.i2c import Bus
import time
import signal

CHANNLE1_BIT = 0x01
CHANNLE2_BIT = 0x02
CHANNLE3_BIT = 0x04
CHANNLE4_BIT = 0x08

CMD_CHANNEL_CTRL = 0x10
CMD_SAVE_I2C_ADDR = 0x11
CMD_READ_I2C_ADDR = 0x12
CMD_READ_FIRMWARE_VER = 0x13

RELAY_ADDR = 0x11


class Grove4chRelay(object):
    def __init__(self, address=RELAY_ADDR):
        self.bus = Bus()
        self.addr = address
        self.channel_state = 0
        self.turn_off_all()

    def __del__(self):
        self.turn_off_all()
        time.sleep(0.1)
        self.bus.close()

    def __exit__(self):
        self.bus.close()

    def getFirmwareVersion(self):
        self._WriteByte(CMD_READ_FIRMWARE_VER, 0)
        return self._ReadByte(CMD_READ_I2C_ADDR)

    def get_state(self):
        bits = [self.channel_state >> i & 1 for i in range(3,-1,-1)]
        return bits[::-1]

    def channel_ctrl(self, state):
        self.channel_state = state
        self._WriteByte(CMD_CHANNEL_CTRL, self.channel_state)

    def turn_on(self, channel):
        self.channel_state |= (1 << (channel - 1))
        self._WriteByte(CMD_CHANNEL_CTRL, self.channel_state)

    def turn_on_all(self):
        self.channel_ctrl(CHANNLE1_BIT | CHANNLE2_BIT |
                          CHANNLE3_BIT | CHANNLE4_BIT)

    def turn_off(self, channel):
        self.channel_state &= ~(1 << (channel - 1))
        self._WriteByte(CMD_CHANNEL_CTRL, self.channel_state)

    def turn_off_all(self):
        self.channel_ctrl(0)

    # read 8 bit data from Reg
    def _ReadByte(self, Reg):
        try:
            read_data = self.bus.read_byte_data(self.addr, Reg)
        except OSError:
            raise OSError(
                "Please check if the I2C device insert in I2C of Base Hat")
        return read_data

    # Write 8 bit data to Reg
    def _WriteByte(self, Reg, Value):
        try:
            self.bus.write_byte_data(self.addr, Reg, Value)
        except OSError:
            raise OSError(
                "Please check if the I2C device insert in I2C of Base Hat")

    # read 16 bit data from Reg
    def _ReadHalfWord(self, Reg):
        try:
            block = self.bus.read_i2c_block_data(self.addr, Reg, 2)
        except OSError:
            raise OSError(
                "Please check if the I2C device insert in I2C of Base Hat")
        read_data = (block[0] & 0xff) | (block[1] << 8)
        return read_data


def main():

    relay = Grove_4ch_relay()
    fwv = relay.getFirmwareVersion()
    print(f"Firmeware Version: {fwv}")

    relay.turn_on(2)
    print(relay.get_state())
    time.sleep(2)

    relay.turn_on(4)
    print(relay.get_state())
    time.sleep(2)

    relay.turn_off_all()
    print(relay.get_state())
    time.sleep(2)

    relay.turn_on_all()
    print(relay.get_state())
    time.sleep(2)

if __name__ == '__main__':
    main()
