import glob
import csv
from datetime import datetime
import os
import shutil

import image_cutter as cut
import detect_occupancy as detect

# Declare system paths
calib = './Calibration Files/IR_closecenter_location.csv'
temp_img = './temp_img/'

# Take photo
# TODO when set up on raspi, right now its just hardcoded
raw_input_image = './Test Images/Ximenes_Phone_IR_closecenter.jpg'

# Process photo using calibration data
cut.cut_image(raw_input_image, calib, temp_img)

# Determine Vacancy and Save to Local Database
imgs = []
for img in glob.glob("{}*.jpg".format(temp_img)):
    imgs.append(img)

imgs = cut.sort_images_by_spotID(imgs)

# Create timestamp and database file
time = datetime.now().strftime("%H_%M_%S")

# Make localdb folder
if not os.path.exists('./localdb/'):
    print("Creating ./localdb/ folder...")
    os.makedirs('./localdb/')

# Create db
f = open('./localdb/{}.csv'.format(time), 'w', newline='')
writer = csv.writer(f)
writer.writerow(['spotID', 'judgement', 'confidence', 'tug', 'dtime', 'tom_conf', 'jerry_conf', 'tweety_conf'])
for img in imgs:
    judgement, confidence, tug, dtime, tom_conf, jerry_conf, tweety_conf = detect.detect_occupancy(img)
    print("=>{} is {} with {:2f} confidence, the tug is {:4f}.".format(img, judgement, confidence, tug))
    writer.writerow([cut.get_spotID(img), judgement, confidence, tug, dtime, tom_conf, jerry_conf, tweety_conf])
f.close()
shutil.rmtree('./temp_img')

# Upload to Cloud Database
