from time import sleep
from picamera import PiCamera
import RPi.GPIO as GPIO

print("Starting up camera...")
camera = PiCamera()
camera.resolution = (4056, 3040)
camera.rotation = 90
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, GPIO.HIGH)

def capture_update():
    # camera.start_preview()
    print("Starting up flash module...")
    GPIO.output(11, GPIO.LOW)
    # Warm up
    sleep(5)
    print("Taking photo, say cheese!")
    camera.capture('./Sorties/Live/Raw/update.jpg')
    print("Photo taken, turning off flash.")
    GPIO.output(11, GPIO.HIGH)
