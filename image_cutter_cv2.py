# Made following https://theailearner.com/tag/cv2-warpperspective/
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Ximenes_Phone test spot
#             [[1420, 1855]],
#             [[1651, 1852]],
#             [[1350, 2043]],
#             [[1616, 2034]]

# load image
img = cv2.imread("./Test Images/Ximenes_Phone.jpg")

#Create copy of image
img_copy = np.copy(img)

img_copy = cv2.cvtColor(img_copy, cv2.COLOR_BGR2RGB)

# plt.imshow(img_copy)
# plt.show()

pt_A = [1420, 1855]
pt_B = [1651, 1852]
pt_C = [1350, 2043]
pt_D = [1616, 2034]

# Find the width and height
width_AD = np.sqrt(((pt_A[0] - pt_D[0]) ** 2) + ((pt_A[1] - pt_D[1]) ** 2))
width_BC = np.sqrt(((pt_B[0] - pt_C[0]) ** 2) + ((pt_B[1] - pt_C[1]) ** 2))
maxWidth = max(int(width_AD), int(width_BC))

height_AB = np.sqrt(((pt_A[0] - pt_B[0]) ** 2) + ((pt_A[1] - pt_B[1]) ** 2))
height_CD = np.sqrt(((pt_C[0] - pt_D[0]) ** 2) + ((pt_C[1] - pt_D[1]) ** 2))
maxHeight = max(int(height_AB), int(height_CD))

# specify point mapping; top left, top right, bottom left, bottom right

input_pts = np.float32([pt_A, pt_C, pt_D, pt_B])
output_pts = np.float32([[0, 0],
                         [0, maxHeight - 1],
                         [maxWidth - 1, maxHeight - 1],
                         [maxWidth - 1, 0]])

#compute transform matrix M
M = cv2.getPerspectiveTransform(input_pts, output_pts)

out = cv2.warpPerspective(img, M, (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)

plt.imshow(out)
plt.show()
cv2.imwrite("test_output_cv2.JPG", out)
