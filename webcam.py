import cv2


def update_photo():
    print('Starting Camera...')
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    while True:
        return_value, image = camera.read()
        print(return_value, image)
        if image is not None:
            break
    cv2.imwrite('./Sorties/Live/Raw/update.jpg', image)
    del camera
    print("Photo updated.")
