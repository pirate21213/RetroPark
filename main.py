import glob
import csv
from datetime import datetime
import os
import shutil

import image_cutter as cut
import detect_occupancy as detect
import comm as comm

# Declare system paths
# calib = './Calibration Files/IR_closecenter_location.csv'
calib = './Sorties/Subscale1/calib.csv'
temp_img = './temp_img/'
cloud_ip = '3.17.147.11'
port = 5001

while True:
    # Clear temp folder if unsafe shutdown happened before
    if os.path.exists("./temp_img"):
        shutil.rmtree('./temp_img')

    # Take photo
    # TODO when set up on raspi, right now its just hardcoded
    # raw_input_image = './Test Images/Ximenes_Phone_IR_closecenter.jpg'
    raw_input_image = './Sorties/Subscale1/Raw/GOPR1855.JPG'

    # Process photo using calibration data
    cut.cut_image(raw_input_image, calib, temp_img)

    # Determine Vacancy and Save to Local Database
    imgs = []
    for img in glob.glob("{}*.jpg".format(temp_img)):
        imgs.append(img)
    imgs = cut.sort_images_by_spotID(imgs)
    print(imgs)

    # Create timestamp and database file
    time = datetime.now().strftime("%H_%M_%S")

    # Make localdb folder
    if not os.path.exists('./localdb/'):
        print("Creating ./localdb/ folder...")
        os.makedirs('./localdb/')

    out_file = './localdb/{}.csv'.format(time)
    # Create db
    f = open(out_file, 'w', newline='')
    writer = csv.writer(f)
    writer.writerow(['spotID', 'judgement', 'confidence', 'tug', 'dtime', 'tom_conf', 'jerry_conf', 'tweety_conf'])
    for img in imgs:
        judgement, confidence, tug, dtime, tom_conf, jerry_conf, tweety_conf = detect.detect_occupancy(img)
        print("=>{} is {} with {:2f} confidence, the tug is {:4f}.".format(img, judgement, confidence, tug))
        writer.writerow([cut.get_spotID(img), judgement, confidence, tug, dtime, tom_conf, jerry_conf, tweety_conf])
    f.close()
    shutil.rmtree('./temp_img')

    # Upload to Cloud Database
    try:
        comm.send_file(out_file, cloud_ip, port)
    except ConnectionRefusedError:
        print("Connection refused, is the cloud listener on?")
    except ConnectionError:
        print("Connection error")
