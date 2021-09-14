import cv2
import csv

# Open the .csv and load their locations into data list
# FORMAT
# spotID, tL_x, tL_y, bL_x, bL_y, bR_x, bR_y, tR_x, tR_y
with open("spot_locations.csv", newline="") as f:
    data = list(csv.reader(f))


# Load the image and whatnot (Hardcoded for testing)
image = cv2.imread("./Test Images/Ximenes_Phone.JPG")
# image = cv2.imread(args["image"])
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
print(data)

for d in data:
    # Place lines for each spot
    cv2.line(image, (d[1], d[2]), (d[3], d[4]), spot_color, thickness=2)
    cv2.line(image, (d[3], d[4]), (d[5], d[6]), spot_color, thickness=2)
    cv2.line(image, (d[5], d[6]), (d[7], d[8]), spot_color, thickness=2)
    cv2.line(image, (d[7], d[8]), (d[1], d[2]), spot_color, thickness=2)

    # Place identifier in the middle of the spot by way of averages
    tX = int((d[1]+d[3]+d[5]+d[7]) / 4)
    tY = int((d[2]+d[4]+d[6]+d[8]) / 4)
    image = cv2.putText(image, "#%d" % d[0], (tX - 20, tY), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1,
                        cv2.LINE_AA)

    # Flip spot color
    if spot_color == red:
        spot_color = blue
    else:
        spot_color = red


while True:
    cv2.imshow("Parking Lot Map", image)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
