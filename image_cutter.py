# Made following https://theailearner.com/tag/cv2-warpperspective/
import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
import csv
from datetime import datetime

# Set up argparse to input the image file location and spot location data
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-d", "--data", required=True, help=".csv file that includes the spot location data")
ap.add_argument("-f", "--folder", required=True, help="Folder path to place generated images such as '.\Output'")
args = vars(ap.parse_args())

maxWidth = 320
maxHeight = 640

# load image
# img = cv2.imread("./Test Images/Ximenes_Phone.jpg", cv2.IMREAD_GRAYSCALE)  #0 reads in as grayscale
img = cv2.imread(args["image"], cv2.IMREAD_GRAYSCALE)

plt.imshow(img, cmap="gray", vmin=0, vmax=255)
plt.show()

# Open the .csv and load their locations into data list
# FORMAT
# spotID, tL_x, tL_y, bL_x, bL_y, bR_x, bR_y, tR_x, tR_y
with open(args["data"], newline="") as f:
    data = list(csv.reader(f))
print("Loaded Spot Location Data:")
print(data)

# Create timestamp
time = datetime.now().strftime("%H_%M_%S")

for d in data:
    # Label current spot
    spotID = d[0]
    # specify point mapping
    input_pts = np.float32([(d[1], d[2]), (d[3], d[4]), (d[5], d[6]), (d[7], d[8]), ])
    output_pts = np.float32([[0, 0],
                             [0, maxHeight - 1],
                             [maxWidth - 1, maxHeight - 1],
                             [maxWidth - 1, 0]])
    # compute transform matrix M
    M = cv2.getPerspectiveTransform(input_pts, output_pts)
    out = cv2.warpPerspective(img, M, (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)

    # plt.imshow(out, cmap="gray", vmin=0, vmax=255)
    # plt.show()
    cv2.imwrite("%s\\%s_%s.jpg" % (args["folder"], spotID, time), out)
    print("%s\\%s_%s.jpg" % (args["folder"], spotID, time))
