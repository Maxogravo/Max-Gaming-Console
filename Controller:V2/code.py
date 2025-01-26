import board
import digitalio
import analogio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

keyboard = Keyboard(usb_hid.devices)

# Button pins
button_pins = {
    "dpad_up": board.GP4,
    "dpad_down": board.GP5,
    "dpad_left": board.GP10,
    "dpad_right": board.GP1,
    "start": board.GP16,
    "select": board.GP21,
    "bottom_face": board.GP7,
    "left_face": board.GP6,
    "top_face": board.GP17,
    "right_face": board.GP9,
    "home": board.GP28,  # New button for "home"
    "ctrl": board.GP13,  # New button for "ctrl"
}

# Key mappings for buttons
key_mapping = {
    "dpad_up": Keycode.UP_ARROW,
    "dpad_down": Keycode.DOWN_ARROW,
    "dpad_left": Keycode.LEFT_ARROW,
    "dpad_right": Keycode.RIGHT_ARROW,
    "start": Keycode.ENTER,
    "select": Keycode.RIGHT_SHIFT,
    "bottom_face": Keycode.Z,
    "left_face": Keycode.X,
    "top_face": Keycode.C,
    "right_face": Keycode.V,
    "home": Keycode.ESCAPE,
    "ctrl": Keycode.SHIFT,
}

# Thumbstick pins
thumbstick_pins = {
    "left_x": board.GP27,  # Left thumbstick X-axis
    "left_y": board.GP26,  # Left thumbstick Y-axis
}

# Thumbstick key mappings
thumbstick_mapping = {
    "left": {"y_pos": Keycode.A, "y_neg": Keycode.D, "x_neg": Keycode.W, "x_pos": Keycode.S},
}

# Initialize buttons
buttons = {}
for name, pin in button_pins.items():
    buttons[name] = digitalio.DigitalInOut(pin)
    buttons[name].direction = digitalio.Direction.INPUT
    buttons[name].pull = digitalio.Pull.UP

# Initialize thumbsticks
thumbsticks = {name: analogio.AnalogIn(pin) for name, pin in thumbstick_pins.items()}

pressed_keys = set()

# Thresholds for thumbstick movement
THUMBSTICK_THRESHOLD = 25000  # Adjust based on observed values
CENTER_THRESHOLD = 32768      # Center of the ADC range

while True:
    # Handle button inputs
    for name, button in buttons.items():
        if not button.value:  # Button pressed
            if name not in pressed_keys:
                keyboard.press(key_mapping[name])
                pressed_keys.add(name)
        else:  # Button released
            if name in pressed_keys:
                keyboard.release(key_mapping[name])
                pressed_keys.remove(name)

    # Handle thumbstick inputs
    for side, axes in [("left", ["x", "y"])]:
        for axis in axes:
            pin_name = f"{side}_{axis}"
            value = thumbsticks[pin_name].value
            axis_map = thumbstick_mapping[side]

            if axis == "x":
                if value < CENTER_THRESHOLD - THUMBSTICK_THRESHOLD:  # Move left
                    if axis_map["x_neg"] not in pressed_keys:
                        keyboard.press(axis_map["x_neg"])
                        pressed_keys.add(axis_map["x_neg"])
                elif value > CENTER_THRESHOLD + THUMBSTICK_THRESHOLD:  # Move right
                    if axis_map["x_pos"] not in pressed_keys:
                        keyboard.press(axis_map["x_pos"])
                        pressed_keys.add(axis_map["x_pos"])
                else:  # Center position
                    for key in [axis_map["x_neg"], axis_map["x_pos"]]:
                        if key in pressed_keys:
                            keyboard.release(key)
                            pressed_keys.remove(key)

            elif axis == "y":
                if value < CENTER_THRESHOLD - THUMBSTICK_THRESHOLD:  # Move up
                    if axis_map["y_neg"] not in pressed_keys:
                        keyboard.press(axis_map["y_neg"])
                        pressed_keys.add(axis_map["y_neg"])
                elif value > CENTER_THRESHOLD + THUMBSTICK_THRESHOLD:  # Move down
                    if axis_map["y_pos"] not in pressed_keys:
                        keyboard.press(axis_map["y_pos"])
                        pressed_keys.add(axis_map["y_pos"])
                else:  # Center position
                    for key in [axis_map["y_neg"], axis_map["y_pos"]]:
                        if key in pressed_keys:
                            keyboard.release(key)
                            pressed_keys.remove(key)
