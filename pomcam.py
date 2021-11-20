from time import sleep
from picamera import PiCamera

print("Starting up camera...")
camera = PiCamera()
camera.resolution = (4056, 3040)
camera.iso = 800

def capture_update():
    # camera.start_preview()
    # Warm up
    sleep(2)
    print("Taking photo, say cheese!")
    camera.capture('./Sorties/Live/Raw/update.jpg')
    print("Photo taken.")
