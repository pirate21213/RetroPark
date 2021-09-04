# Made following https://jdhao.github.io/2019/02/23/crop_rotated_rectangle_opencv/
import numpy as np
import cv2

img = cv2.imread("./Test Images/Ximenes_Phone.JPG")
# points for test rectangle
bound = np.array([               # These coordinates are what we would need to create at first setup
            [[1420, 1855]],
            [[1651, 1852]],
            [[1350, 2043]],
            [[1616, 2034]]
        ])
print("Shape of bound: {}".format(bound.shape))
rect = cv2.minAreaRect(bound)
print("rect: {}".format(rect))

box = cv2.boxPoints(rect)
box = np.int0(box)

print("bounding box: {}".format(box))
cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

width = int(rect[1][0])
height = int(rect[1][1])

src_pts = box.astype("float32")

dst_pts = np.array([[0, width-1],
                   [0, 0],
                   [height-1, 0],
                   [height-1, width-1]], dtype="float32")

M = cv2.getPerspectiveTransform(src_pts, dst_pts)
warped = cv2.warpPerspective(img, M, (width, height))
cv2.imwrite("test_output.JPG", warped)
