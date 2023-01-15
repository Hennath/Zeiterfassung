import mfrc522
from flask import current_app
from app import app
from threading import Thread
import time

# Custom RFID reader class with added rfid_scan method
class CustomMFRC522(mfrc522.SimpleMFRC522):

    # rfid_scan method. Watches for rfid tag for provided amount of seconds
    def rfid_scan(self, seconds):
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time
            code = self.read_id_no_block()
            if code:
                print("tag detected!")
                return code  
            
            if elapsed_time > seconds:
                print("No tag detected!")
                break

                
