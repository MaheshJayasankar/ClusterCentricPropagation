from PIL import Image
import os

# File contains operations involving creation of thumbnails

# ---------------------------------
# Internal functions
# ---------------------------------
# Converts an image to specified dimensions but maintaining aspect ratio. Extra canvas space is filled as black
def ReduceImageToDimensions(img: Image,thumb_size):
    pix = img.load()
    newImage = Image.new(mode = "RGB", size = thumb_size)
    (oldWidth, oldHeight) = img.size
    x1 = (int)((thumb_size[0] - oldWidth) / 2)
    y1 = (int)((thumb_size[1] - oldHeight) / 2)
    newImage.paste(img, (x1,y1,x1+oldWidth,y1+oldHeight))
    img = newImage
    return img

# ---------------------------------
# External functions
# ---------------------------------
# Performs MakeThumbSize operation on all png files in a given folder.
def ReduceImagesInFolderToDimensions(base_dir, thumb_size):
    for f in os.listdir(base_dir):
        if f.endswith('.png'):
            img = Image.open(base_dir+'/{}'.format(f))
            img = ReduceImageToDimensions(img, thumb_size)
            img.save(base_dir+'/{}'.format(f))
