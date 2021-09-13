import cv2
import argparse

# Set up argparse to input the image file location
ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

# Draws a non uniform rectangle and returns the coordinates of the four points, must be click in counter clockwise order
# Starting from the top left (Corner 0 is top left, corner 1 is bottom left, etc)
# clear spot_selections TODO - Replace this with a file reader that places lines around the spots and their IDs
fo = open("spot_locations.csv", "w")
fo.close()

refPt = []
corner = 0
spot_id = 0
blue = (255, 0, 0)
red = (0, 0, 255)
spot_color = red


def select_spot(event, x, y, flags, param):
    global refPt, corner, clone, spot_id

    # Point saving
    if event == cv2.EVENT_LBUTTONDOWN and corner == 0:
        refPt = [(x, y)]
        clone = image.copy()
    elif event == cv2.EVENT_LBUTTONDOWN and corner == 1:
        refPt.append((x, y))
    elif event == cv2.EVENT_LBUTTONDOWN and corner == 2:
        refPt.append((x, y))
    elif event == cv2.EVENT_LBUTTONDOWN and corner == 3:
        refPt.append((x, y))

    # Line Drawing
    elif event == cv2.EVENT_LBUTTONUP and corner == 0:
        corner = 1
    elif event == cv2.EVENT_LBUTTONUP and corner == 1:
        cv2.line(image, refPt[0], refPt[1], spot_color, thickness=2)
        corner = 2
    elif event == cv2.EVENT_LBUTTONUP and corner == 2:
        cv2.line(image, refPt[1], refPt[2], spot_color, thickness=2)
        corner = 3
    elif event == cv2.EVENT_LBUTTONUP and corner == 3:
        cv2.line(image, refPt[2], refPt[3], spot_color, thickness=2)
        cv2.line(image, refPt[3], refPt[0], spot_color, thickness=2)
        # corner = 0


# Load the image and whatnot (Hardcoded for testing)
image = cv2.imread("./Test Images/Ximenes_Phone.JPG")
# image = cv2.imread(args["image"])
scale_percent = 30  # percent of original size
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
clone = image.copy()
cv2.namedWindow("Parking Lot Map")
cv2.setMouseCallback("Parking Lot Map", select_spot)

# Keep looping until q key is press
while True:
    cv2.imshow("Parking Lot Map", image)
    key = cv2.waitKey(1) & 0xFF

    # Reset current selection
    if key == ord("r"):
        image = clone.copy()
        corner = 0
        refPt = []

    elif key == ord(" "):
        # File io setup
        fo = open("spot_locations.csv", "a")
        # spotID, tL_x, tL_y, bL_x, bL_y, bR_x, bR_y, tR_x, tR_y
        unscale = 100 / scale_percent
        fo.write("%d,%d,%d,%d,%d,%d,%d,%d,%d\n" % (spot_id,
                                                   refPt[0][0] * unscale, refPt[0][1] * unscale,
                                                   refPt[1][0] * unscale, refPt[1][1] * unscale,
                                                   refPt[2][0] * unscale, refPt[2][1] * unscale,
                                                   refPt[3][0] * unscale, refPt[3][1] * unscale))
        fo.close()

        # Place identifier in the middle of the spot by way of averages
        tX = int((refPt[0][0]+refPt[1][0]+refPt[2][0]+refPt[3][0])/4)
        tY = int((refPt[0][1]+refPt[1][1]+refPt[2][1]+refPt[3][1])/4)
        image = cv2.putText(image, "#%d" % spot_id, (tX-20, tY), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        spot_id += 1

        # Swap color between blue and red for readability
        if spot_color == red:
            spot_color = blue
        else:
            spot_color = red

        corner = 0

    # Break from the loop and do the stuff, probably going to change this flow
    elif key == ord("q"):

        break
