#!/usr/bin/python
import pynput.keyboard

def process_keys(key):
    print(key)


keyboard_listener = pynput.keyboard.Listener(on_press = process_keys)
with keyboard_listener:
    keyboard_listener.join()
