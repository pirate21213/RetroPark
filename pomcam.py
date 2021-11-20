from time import sleep
from picamera import PiCamera


def capture_update():
    print("Starting up camera...")
    camera = PiCamera()
    camera.resolution = (4056, 3040)
    camera.iso = 800
    # camera.start_preview()
    # Warm up
    sleep(2)
    print("Taking photo, say cheese!")
    camera.capture('./Sorties/Live/update.jpg')
    print("Photo taken.")
