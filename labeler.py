# Display a sequential list of images, label and sort them into appropriate folders
# DEMO: python .\labeler.py -i .\Output\ -o .\SortTest\Sorted\

import glob
import os
import cv2
import argparse
from datetime import datetime

# Set up argparse to input the image file location
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input_folder", required=True, help="Path to the folder with the images")
ap.add_argument("-o", "--output_folder", required=True, help="Path to the output folder")
args = vars(ap.parse_args())

# Make output folders if they don't exist
occ = os.path.join(args["output_folder"], "occ")
nocc = os.path.join(args["output_folder"], "nocc")
if not os.path.exists(os.path.join(args["output_folder"], "occ")):
    os.makedirs(occ)
if not os.path.exists(os.path.join(args["output_folder"], "nocc")):
    os.makedirs(nocc)

images = []

scale_percent = 30  # percent of original size
images = [cv2.imread(file) for file in glob.glob("{}*.jpg".format(args["input_folder"]))]

# Create timestamp
time = datetime.now().strftime("%H_%M_%S")
count = 0

for image in images:
    while True:
        cv2.namedWindow("[U]noccupied or [O]ccupied")
        cv2.imshow("[U]noccupied or [O]ccupied", image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            quit()
        if key == ord("u"):
            cv2.imwrite(os.path.join(nocc, "nocc_%s_%s.jpg" % (time, count)), image)
            count += 1
            break
        if key == ord("o"):
            cv2.imwrite(os.path.join(occ, "occ_%s_%s.jpg" % (time, count)), image)
            count += 1
            break



