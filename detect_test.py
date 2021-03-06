import glob

from detect_occupancy import detect_occupancy

imgs = []
for img in glob.glob("./Processed Images/*.jpg"):
    imgs.append(img)
imgs.sort()
for img in imgs:
    judgement, confidence, tug, dtime = detect_occupancy(img)
    print("=>{} is {} with {:2f} confidence, the tug is {:4f}.".format(img, judgement, confidence, tug))
print("{} spots analyzed over {:4f} seconds".format(len(imgs), total_time))

