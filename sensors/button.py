from grove.button import Button
from grove.factory import Factory


class GroveButton(object):
    def __init__(self, pin):
        # High = pressed
        self.__btn = Factory.getButton("GPIO-HIGH", pin)
        self.__pressed = False
        self.__on_press = None
        self.__on_release = None
        self.__btn.on_event(self, GroveButton.__handle_event)

    @property
    def on_press(self):
        return self.__on_press

    @on_press.setter
    def on_press(self, callback):
        if not callable(callback):
            return
        self.__on_press = callback

    @property
    def on_release(self):
        return self.__on_release

    @on_release.setter
    def on_release(self, callback):
        if not callable(callback):
            return
        self.__on_release = callback

    def __handle_event(self, evt):
        if evt["code"] == Button.EV_LEVEL_CHANGED:
            if evt["pressed"]:
                if not self.__pressed and callable(self.__on_press):
                    self.__pressed = True
                    self.__on_press()
            else:
                if self.__pressed and callable(self.__on_release):
                    self.__pressed = False
                    self.__on_release()
