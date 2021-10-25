import cv2
import csv
import argparse

# Set up argparse to input the image file location and spot location data
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-d", "--data", required=True, help=".csv file that includes the spot location data")
args = vars(ap.parse_args())

# Open the .csv and load their locations into data list
# FORMAT
# spotID, tL_x, tL_y, bL_x, bL_y, bR_x, bR_y, tR_x, tR_y
with open(args["data"], newline="") as f:
    data = list(csv.reader(f))
# print("Loaded Spot Location Data:")
# print(data)


# Load the image and whatnot (Hardcoded for testing)
# image = cv2.imread("./Test Images/Ximenes_Phone.JPG")
image = cv2.imread(args["image"])
scale_percent = 20  # percent of original size
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
clone = image.copy()
cv2.namedWindow("Parking Lot Map")
blue = (255, 0, 0)
red = (0, 0, 255)
spot_color = red

# Convert data list to int with scaling and ignoring spotID
for d in data:
    for i in range(0, len(d)):
        d[i] = int(d[i])
        if i != 0:
            d[i] = int(d[i] * scale_percent / 100)

for d in data:
    # Place lines for each spot
    cv2.line(image, (d[1], d[2]), (d[3], d[4]), spot_color, thickness=2)
    cv2.line(image, (d[3], d[4]), (d[5], d[6]), spot_color, thickness=2)
    cv2.line(image, (d[5], d[6]), (d[7], d[8]), spot_color, thickness=2)
    cv2.line(image, (d[7], d[8]), (d[1], d[2]), spot_color, thickness=2)

    # Place identifier in the middle of the spot by way of averages
    tX = int((d[1]+d[3]+d[5]+d[7]) / 4)
    tY = int((d[2]+d[4]+d[6]+d[8]) / 4)
    image = cv2.putText(image, "#%d" % d[0], (tX - 10, tY), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 1,
                        cv2.LINE_AA)

    # Swap color between blue and red for readability
    spot_color = red if spot_color == blue else blue


while True:
    cv2.imshow("Parking Lot Map", image)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
