import threading
from mfrc522_custom import CustomMFRC522
#import mfrc522_custom 

reader = CustomMFRC522()

def on_tag_detected(tag_id):
    print("Tag detected:", tag_id)

# Create a new thread that listens for events from the reader
listener = threading.Thread(target=reader.listen, args=(on_tag_detected,))

# Start the listener thread
listener.start()
