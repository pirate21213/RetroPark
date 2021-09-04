import PIL as pillow
from PIL import Image
from PIL import ImageOps
import glob

# Test file to see how well pillow can do image manipulation

for infile in glob.glob("./Test Images/Ximenes_Phone.JPG"):
    outfile = "test_output.JPG"
    with Image.open(infile) as im:  # im is image object
        ImageOps.grayscale(im).show()
        ImageOps.grayscale(im).save(outfile)
        print(im.getPixel((1421,1854)))


