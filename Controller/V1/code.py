import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

keyboard = Keyboard(usb_hid.devices)

# pinsssss lol
button_pins = {
    "dpad_up": board.GP5,
    "dpad_down": board.GP3,
    "dpad_left": board.GP27,
    "dpad_right": board.GP0,
    "start": board.GP16,
    "select": board.GP22,
    "bottom_face": board.GP15, 
    "left_face": board.GP9, 
    "top_face": board.GP17,   
    "right_face": board.GP12, 
}

# Keyssss lmao
key_mapping = {
    "dpad_up": Keycode.UP_ARROW,
    "dpad_down": Keycode.DOWN_ARROW,
    "dpad_left": Keycode.LEFT_ARROW,
    "dpad_right": Keycode.RIGHT_ARROW,
    "start": Keycode.ENTER,
    "select": Keycode.RIGHT_SHIFT,
    "bottom_face": Keycode.A,
    "left_face": Keycode.S,
    "top_face": Keycode.D,
    "right_face": Keycode.F,
}


buttons = {}
for name, pin in button_pins.items():
    buttons[name] = digitalio.DigitalInOut(pin)
    buttons[name].direction = digitalio.Direction.INPUT
    buttons[name].pull = digitalio.Pull.UP 


pressed_keys = set()

while True:
    for name, button in buttons.items():
        if not button.value:  
            if name not in pressed_keys:
                keyboard.press(key_mapping[name])
                pressed_keys.add(name)
        else: 
            if name in pressed_keys:
                keyboard.release(key_mapping[name])
                pressed_keys.remove(name)
                


