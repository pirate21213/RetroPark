from time import sleep
from picamera import PiCamera


def capture_update():
    camera = PiCamera()
    camera.resolution = (4056, 3040)
    camera.iso = 800
    camera.start_preview()
    # Warm up
    sleep(2)
    camera.capture('./Sorties/Live/update.jpg')
