import mfrc522
from flask import current_app
from app import app
from threading import Thread
import time

class CustomMFRC522(mfrc522.SimpleMFRC522):
    # This class subclasses SimpleMFRC522 and adds a new listen method.

    # def listen(self, on_tag_detected):
    #     # This function will be called by the thread to listen for events
    #     # from the RFID reader.
    #     while True:
    #         # Check for a new tag
    #         id, text = self.read()
    #         print("reading.............")

    #         # If a tag is detected, call the callback function
    #         if id:
    #             on_tag_detected(id)

    def rfid_scan(self, seconds):
        start_time = time.time()
        counter = 1
        while True:
            elapsed_time = time.time() - start_time
            code = self.read_id_no_block()
            if code:
                print("Code found!")
                return code  
            
            if elapsed_time > seconds:
                print("BREAK")
                break
            print(f"test#{counter}")
            counter+=1

    def listen(self, on_tag_detected):
        # Start a new thread to listen for events from the RFID reader.
        thread = Thread(target=self._listen, args=(on_tag_detected,))
        thread.start()

    def _listen(self, on_tag_detected):
        # This function will be called by the thread to listen for events
        # from the RFID reader.
        while True:
            # Check for a new tag
            id, text = self.read()
            print("reading.............")

            # If a tag is detected, call the callback function
            if id:
                on_tag_detected(id,)
                
