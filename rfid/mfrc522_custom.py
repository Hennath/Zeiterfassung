import mfrc522
from flask import current_app
from app import app
from threading import Thread

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
                
