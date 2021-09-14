# Made following https://theailearner.com/tag/cv2-warpperspective/
import cv2
import numpy as np
import matplotlib.pyplot as plt

maxWidth = 320
maxHeight = 640

# Ximenes_Phone test spot 1 (Unoccupied)
#             [[1420, 1855]],
#             [[1651, 1852]],
#             [[1350, 2043]],
#             [[1616, 2034]]
# Ximenes_Phone test spot 2 (Unoccupied)
#             [[2820, 1464]],
#             [[2957, 1466]],
#             [[2894, 1549]],
#             [[3069, 1549]]
# Ximenes_Phone test spot 3 (Occupied)
#             [[2098, 1847]],
#             [[2326, 1844]],
#             [[2137, 2026]],
#             [[2398, 2024]]
# Ximenes_Phone test spot 4 (Partial Occlusion - Unoccupied)
#             [[2075, 1706]],
#             [[2270, 1707]],
#             [[2099, 1847]],
#             [[2326, 1843]]

# load image
img = cv2.imread("./Test Images/Ximenes_Phone.jpg", cv2.IMREAD_GRAYSCALE)  #0 reads in as grayscale

plt.imshow(img, cmap="gray", vmin=0, vmax=255)
plt.show()

# The following can/should be reduced into a series of for loops

pt_A = [1420, 1855]
pt_B = [1651, 1852]
pt_C = [1350, 2043]
pt_D = [1616, 2034]

# specify point mapping; I did top left, top right, bottom left, bottom right; input wants top left counter clockwise
input_pts = np.float32([pt_A, pt_C, pt_D, pt_B])
output_pts = np.float32([[0, 0],
                         [0, maxHeight - 1],
                         [maxWidth - 1, maxHeight - 1],
                         [maxWidth - 1, 0]])

# compute transform matrix M
M = cv2.getPerspectiveTransform(input_pts, output_pts)

out = cv2.warpPerspective(img, M, (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)

plt.imshow(out, cmap="gray", vmin=0, vmax=255)
plt.show()
cv2.imwrite("test_output_warped_1.JPG", out)

pt_A = [2820, 1464]
pt_B = [2957, 1466]
pt_C = [2894, 1549]
pt_D = [3069, 1549]

# specify point mapping; I did top left, top right, bottom left, bottom right; input wants top left counter clockwise
input_pts = np.float32([pt_A, pt_C, pt_D, pt_B])
output_pts = np.float32([[0, 0],
                         [0, maxHeight - 1],
                         [maxWidth - 1, maxHeight - 1],
                         [maxWidth - 1, 0]])

# compute transform matrix M
M = cv2.getPerspectiveTransform(input_pts, output_pts)

out = cv2.warpPerspective(img, M, (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)

plt.imshow(out, cmap="gray", vmin=0, vmax=255)
plt.show()
cv2.imwrite("test_output_warped_2.JPG", out)

pt_A = [2098, 1847]
pt_B = [2326, 1844]
pt_C = [2137, 2026]
pt_D = [2398, 2024]

# specify point mapping; I did top left, top right, bottom left, bottom right; input wants top left counter clockwise
input_pts = np.float32([pt_A, pt_C, pt_D, pt_B])
output_pts = np.float32([[0, 0],
                         [0, maxHeight - 1],
                         [maxWidth - 1, maxHeight - 1],
                         [maxWidth - 1, 0]])

# compute transform matrix M
M = cv2.getPerspectiveTransform(input_pts, output_pts)

out = cv2.warpPerspective(img, M, (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)

plt.imshow(out, cmap="gray", vmin=0, vmax=255)
plt.show()
cv2.imwrite("test_output_warped_3.JPG", out)

pt_A = [2075, 1706]
pt_B = [2270, 1707]
pt_C = [2099, 1847]
pt_D = [2326, 1843]

# specify point mapping; I did top left, top right, bottom left, bottom right; input wants top left counter clockwise
input_pts = np.float32([pt_A, pt_C, pt_D, pt_B])
output_pts = np.float32([[0, 0],
                         [0, maxHeight - 1],
                         [maxWidth - 1, maxHeight - 1],
                         [maxWidth - 1, 0]])

# compute transform matrix M
M = cv2.getPerspectiveTransform(input_pts, output_pts)

out = cv2.warpPerspective(img, M, (maxWidth, maxHeight), flags=cv2.INTER_LINEAR)

plt.imshow(out, cmap="gray", vmin=0, vmax=255)
plt.show()
cv2.imwrite("test_output_warped_4.JPG", out)
#             [[2075, 1706]],
#             [[2270, 1707]],
#             [[2099, 1847]],
#             [[2326, 1843]]