import cv2
import argparse

# Set up argparse to input the image file location
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-o", "--output", required=True, help=".csv file to output spot location data to")
args = vars(ap.parse_args())

# Global variable definitions
refPt = []  # list that will hold the 4 2-tuples of the spot corners, cleared each spot
corner = 0  # which corner is currently being selected; state machine that drives the selection
spot_id = 0  # running number that identifies each spot, counts from 0 up
blue = (255, 0, 0)  # constant blue BGR code
red = (0, 0, 255)  # constant red BGR code
spot_color = red  # variable that tracks which color to currently draw the spot in, flips between red and blue

# Create output file, CAUTION if it already exists then it will be cleared
fo = open(args["output"], "w")
fo.close()


# This function is called each time a mouse event is passed by cv2
def select_spot(event, x, y, flags, param):
    global refPt, corner, clone, spot_id  # redefine these variables as global

    # Point saving, on the rising edge of a left mouse click check which corner is currently being selected and save
    # the coords to refPt. On the falling edge corner is updated and the line is drawn if applicable
    if event == cv2.EVENT_LBUTTONDOWN and corner == 0:
        refPt = [(x, y)]  # clears the list and places only the first set of coords in it
        clone = image.copy()  # save the image before drawing any lines, this allows a reset to work
    elif event == cv2.EVENT_LBUTTONDOWN and corner == 1:
        refPt.append((x, y))  # appends the next set of coords to the list
    elif event == cv2.EVENT_LBUTTONDOWN and corner == 2:
        refPt.append((x, y))
    elif event == cv2.EVENT_LBUTTONDOWN and corner == 3:
        refPt.append((x, y))

    # Line Drawing, on the falling edge of a mouse click the corner is updated and the line is drawn
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
        # corner is not set to 0 here, instead it is set to 0 when space is pressed to allow you to confirm the spot


# Load the image and whatnot (Hardcoded for testing)
# image = cv2.imread("./Test Images/Ximenes_Phone.JPG")
image = cv2.imread(args["image"])
scale_percent = 100  # percent of original size
width = int(image.shape[1] * scale_percent / 100)  # scale the image based on the percentage
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)  # scaled image
clone = image.copy()
cv2.namedWindow("Parking Lot Map")
cv2.setMouseCallback("Parking Lot Map", select_spot)  # set mousecallback event to call select_spot function

# Keep looping until q key is press
while True:
    cv2.imshow("Parking Lot Map", image)
    key = cv2.waitKey(1) & 0xFF

    # Reset current selection
    if key == ord("r"):
        image = clone.copy()
        corner = 0
        refPt = []

    # whenever space is pressed confirm the selections and add the coordinates to the csv
    elif key == ord(" "):
        # File io setup
        fo = open(args["output"], "a")
        # spotID, tL_x, tL_y, bL_x, bL_y, bR_x, bR_y, tR_x, tR_y
        unscale = 100 / scale_percent  # use the same scale percentage to unscale the coordinates to their raw values
        fo.write("%d,%d,%d,%d,%d,%d,%d,%d,%d\n" % (spot_id,
                                                   refPt[0][0] * unscale, refPt[0][1] * unscale,
                                                   refPt[1][0] * unscale, refPt[1][1] * unscale,
                                                   refPt[2][0] * unscale, refPt[2][1] * unscale,
                                                   refPt[3][0] * unscale, refPt[3][1] * unscale))
        fo.close()

        # Place identifier in the middle of the spot by way of averages
        tX = int((refPt[0][0] + refPt[1][0] + refPt[2][0] + refPt[3][0]) / 4)
        tY = int((refPt[0][1] + refPt[1][1] + refPt[2][1] + refPt[3][1]) / 4)
        image = cv2.putText(image, "#%d" % spot_id, (tX - 10, tY), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1,
                            cv2.LINE_AA)
        spot_id += 1
        corner = 0
        # Swap color between blue and red for readability
        spot_color = red if spot_color == blue else blue


    # Break from the loop and do the stuff, probably going to change this flow
    elif key == ord("q"):
        break
