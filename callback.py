import threading
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

def on_tag_detected(tag_id):
    print("Tag detected:", tag_id)

# Create a new thread that listens for events from the reader
listener = threading.Thread(target=reader.listen, args=(on_tag_detected,))

# Start the listener thread
listener.start()
