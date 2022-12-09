#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

# reader = SimpleMFRC522()
# try:
#         id, text = reader.read()
#         print(id)
#         print(text)
# finally:
#         GPIO.cleanup()


def read():
    reader = SimpleMFRC522()
    try:
        id, text = reader.read()
        print(id)
        print(text)
        return id
    finally:
        GPIO.cleanup()
