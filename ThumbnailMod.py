from PIL import Image
import os

thumb_size = (512,512)

def MakeThumbSize(img: Image,thumb_size):
    pix = img.load()
    newImage = Image.new(mode = "RGB", size = thumb_size)
    (oldWidth, oldHeight) = img.size
    x1 = (int)((thumb_size[0] - oldWidth) / 2)
    y1 = (int)((thumb_size[1] - oldHeight) / 2)
    newImage.paste(img, (x1,y1,x1+oldWidth,y1+oldHeight))
    img = newImage
    return img


def MakeThumbSizeCanvasInFolder(thumb_size, base_dir):
    for f in os.listdir(base_dir):
        if f.endswith('.png'):
            img = Image.open(base_dir+'/{}'.format(f))
            img = MakeThumbSize(img, thumb_size)
            img.save(base_dir+'/{}'.format(f))
