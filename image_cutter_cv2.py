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
