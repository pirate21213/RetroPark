# Made following https://theailearner.com/tag/cv2-warpperspective/
import cv2
import numpy as np
import csv
import os
from datetime import datetime


def cut_image(image_path, calib_data, output_dir):
    # Make output folder
    if not os.path.exists(output_dir):
        print("Creating output folder...")
        os.makedirs(output_dir)

    maxWidth = 320
    maxHeight = 640

    # load image
    # img = cv2.imread("./Test Images/Ximenes_Phone.jpg", cv2.IMREAD_GRAYSCALE)  #0 reads in as grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Open the .csv and load their locations into data list
    # FORMAT
    # spotID, tL_x, tL_y, bL_x, bL_y, bR_x, bR_y, tR_x, tR_y
    with open(calib_data, newline="") as f:
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
        cv2.imwrite("%s\\%s_%s.jpg" % (output_dir, spotID, time), out)
        print("Creating %s\\%s_%s.jpg" % (output_dir, spotID, time))


def sort_images_by_spotID(image_list):
    # assumes spotID starts at 0, honestly a booboo way of sorting but it works in this context
    # Although, this does have some merit as it is capable of sorting duplicates of the same spotID
    sorted_image_list = []
    num = 0
    while len(image_list) != len(sorted_image_list):
        print("looking for number {}".format(num))
        for img in image_list:
            spotID = get_spotID(img)
            #print(get_spotID(img))
            if spotID == num:
                print("Found it, sorting...")
                sorted_image_list.append(img)
        num += 1
    return sorted_image_list


def get_spotID(image):
    return int(str(os.path.basename(image)).split(sep='_', maxsplit=1)[0].replace('\\', ''))
