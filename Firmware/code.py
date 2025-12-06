# KMK firmware for Hackpad (XIAO RP2040)
# Features: 4 keys, rotary encoder, 4 SK6812 RGB LEDs

import board
import supervisor
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.extensions.encoder import EncoderHandler
from kmk.extensions.peg_rgb import RGB

keyboard = KMKKeyboard()

# --- Key Pins ---
keyboard.col_pins = ()  
keyboard.row_pins = (board.A0, board.A1, board.A2, board.A3) 
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# --- Keymap ---
from kmk.handlers.sequences import send_string
from kmk.handlers.sequences import simple_key_sequence
from kmk.handlers.sequences import send_combination
from kmk.handlers import HandlerResult
from kmk.keys import make_key
import time
import supervisor

# --- Keymap with custom actions ---
def mute_spotify(key, keyboard, *args, **kwargs):
    keyboard.send(KC.AUDIO_MUTE)
    return HandlerResult(True)

def new_firefox_window(key, keyboard, *args, **kwargs):
    keyboard.send(KC.LCTRL(KC.N))
    return HandlerResult(True)

keyboard.keymap = [
    [make_key(mute_spotify), make_key(new_firefox_window), KC.C, KC.D],
]

# --- Rotary Encoder ---
encoder = EncoderHandler()
encoder.pins = ((board.SDA, board.SCL, None),)  
encoder.map = [
    ((KC.VOLU, KC.VOLD),),  
]
keyboard.extensions.append(encoder)

# --- RGB LEDs (SK6812/NeoPixel) ---
rgb = RGB(
    pixel_pin=board.TX,  
    num_pixels=4,
    rgb_order=(1, 0, 2), 
    auto_write=True,
)
keyboard.extensions.append(rgb)


# --- Per-key LED lighting ---
from kmk.handlers import on_press, on_release
import neopixel

NUM_LEDS = 4
PIXEL_PIN = board.TX
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_LEDS, auto_write=True, pixel_order=(1,0,2))

def light_led(idx, color=(0, 50, 0)):
    pixels[idx] = color

def clear_led(idx):
    pixels[idx] = (0, 0, 0)

@on_press
def handle_press(key, keyboard, *args, **kwargs):
    if key in keyboard.keymap[0]:
        idx = keyboard.keymap[0].index(key)
        light_led(idx)
    return HandlerResult(True)

@on_release
def handle_release(key, keyboard, *args, **kwargs):
    if key in keyboard.keymap[0]:
        idx = keyboard.keymap[0].index(key)
        clear_led(idx)
    return HandlerResult(True)

keyboard.on_press(handle_press)
keyboard.on_release(handle_release)

if __name__ == '__main__':
    keyboard.go()
