import time
from sensors import GroveButton, Grove4chRelay

def main():
    button = GroveButton(12)
    relay = Grove4chRelay(0x11)

    def on_press():
        relay.turn_on_all()
        # relay.turn_on(1)
    button.on_press = on_press

    def on_release():
        relay.turn_off_all()
    button.on_release = on_release

    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
