from PIL import Image
import os

size_1024 = (1024,1024)

for f in os.listdir('.'):
    print('going through ' + f)
    if (f.endswith('.jpg')):
        i = Image.open(f)
        fn , fext = os.path.splitext(f)
        i.thumbnail(size_1024)
        i.save('thumbnails/{}_1024.png'.format(fn))