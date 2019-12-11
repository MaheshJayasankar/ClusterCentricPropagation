from PIL import Image
import os
import ThumbnailMod
import PalFinder
import GifCreator
import random
import math
import time

#........................................
# Input Specifications
#........................................

baseImgDirectory = "baseimages"
processedImgDirectory = "processedimages"
outputDirectory = "outputgifs"
thumb_size = (512, 512)
thumb_len = 512
pal_count = 16
pal_img_scale = 8
extra_gif_frames = 12
should_standardize_size = True

#-----------------------
#algorithm parameters
#-----------------------

iter_count = 30000000
cluster_pull_strength = 25
cluster_pull_falloff = 3
use_falloff = True
pal_count = 16
seed = 0
total_steps = 30

#........................................
# Preprocessing Checks
#........................................

if not(os.path.exists(baseImgDirectory)):
    os.makedirs(baseImgDirectory)
if not(os.path.exists(processedImgDirectory)):
    os.makedirs(processedImgDirectory)
if not(os.path.exists(outputDirectory)):
    os.makedirs(outputDirectory)

#........................................
# Main algorithm
#........................................

def ProcessImage(srcimg, fn, dest):
    iter_check = iter_count / total_steps

    random.seed(seed)
    img_size = srcimg.size
    max_sqr_dist = srcimg.size[0] * srcimg.size[0] + srcimg.size[1] * srcimg.size[1]

    (palList, palModeImg) = PalFinder.getPalColours(srcimg, pal_count)
    palModeImg.save(dest+'/'+fn+'/paletted'+fn+'.png')
    palImg = PalFinder.MakePalImg(pal_count, palList, pal_img_scale)
    print(fn+': Image Paletted')
    if not os.path.exists(dest+'/{}/steps'.format(fn)):
        os.makedirs(dest+'/{}/steps'.format(fn))
    palImg.save(dest+'/{}/palette.png'.format(fn))
    palPixels = palModeImg.load()

    pixels = srcimg.load()
    boxSize = 8
    clusterimg = Image.new('RGB', srcimg.size)
    meanCoordList = list()
    for i in range(pal_count):
        meanCoord = PalFinder.GetMeanOfColInImage(palModeImg, palList, palList[i])
        meanCoordList.append(meanCoord)
        clusterimg = PalFinder.DrawBox(clusterimg, meanCoord, boxSize, palList[i])

    print(fn+': Image cluster generated')
    clusterimg.save(dest+'/{}/cluster.png'.format(fn))
    skiplog = 0

    print(fn+': Processing Image',end='', flush = True)

    start_time = time.time()

    for iter in range(iter_count):
        x = random.randint(0, img_size[0] - 1)
        y = random.randint(0, img_size[1] - 1)
        palIndex = palPixels[x,y]
        meanCoord = meanCoordList[palIndex]
        (deltaFromMeanX, deltaFromMeanY) = (x- meanCoord[0], y - meanCoord[1])
        dist_from_mean = math.sqrt(deltaFromMeanX*deltaFromMeanX + deltaFromMeanY*deltaFromMeanY)
        if (dist_from_mean <= 0):
            skiplog+=1
            continue
        sqr_dist = (x-meanCoord[0])*(x-meanCoord[0]) + (y-meanCoord[1])*(y-meanCoord[1])
        falloff = 1
        if (use_falloff):
            falloff = (1-(sqr_dist / max_sqr_dist))
            for i in range(cluster_pull_falloff):
                falloff*=falloff
            falloff = (1-(1/(2-falloff)))
        dist = cluster_pull_strength * falloff
        rawDeltaX = dist * deltaFromMeanX / dist_from_mean
        rawDeltaY = dist * deltaFromMeanY / dist_from_mean

        deltaX = math.ceil(rawDeltaX)
        deltaY = math.ceil(rawDeltaY)

        x2 = PalFinder.clamp(x - deltaX,0,img_size[0]- 1)
        y2 = PalFinder.clamp(y - deltaY, 0, img_size[1] - 1)
        #swap
        temp1 = pixels[x2,y2]
        temp2 = palPixels[x2,y2]
        pixels[x2,y2] = pixels[x,y]
        palPixels[x2,y2] = palPixels[x,y]
        pixels[x,y] = temp1
        palPixels[x,y] = temp2

        if (iter)%iter_check == 0:
            print('.',end='', flush = True)
            srcimg.save(dest+'/'+fn+'/steps/'+str((int)(iter/iter_check))+'.png')
    srcimg.save(dest+'/'+fn+'/steps/'+str((int)(total_steps))+'.png')
    end_time = time.time()
    delta_time = end_time - start_time
    time_per_step = delta_time / total_steps
    time_per_iter = delta_time / iter_count
    print('\n'+fn+': Processing finished.\n Total Iterations:', iter_count, 'Iterations Wasted:',skiplog)
    print('Total time taken:', "{:0.2f}".format(delta_time),"\nTime per step:","{:0.2f}".format(time_per_step),"\nTime per iteration","{:0.2E}".format(time_per_iter))
    srcimg.save(dest+'/{}/final.png'.format(fn))

#........................................
# Start of Main Control Loop
#........................................

flag = False
for f in os.listdir(baseImgDirectory):
    if (f.endswith('.png') or f.endswith('.jpg')):
        flag = True
        (fn, fext) = os.path.splitext(f)
        if (os.path.exists(processedImgDirectory+'/'+ fn)):
            print('Folder named',fn,'already exists. Delete or move the folder to process this image.')
            continue
        os.makedirs(processedImgDirectory+'/'+fn)
        i = Image.open(baseImgDirectory+'/'+ f)
        if (i.size[0] > thumb_len or i.size[1] > thumb_len):
            i.thumbnail(thumb_size)
        i.save(processedImgDirectory+'/'+fn+'/'+fn+'.png')
        print('Processing begins for {}'.format(fn))
        ProcessImage(i, fn, processedImgDirectory)
        steps_folder = processedImgDirectory+'/{}/steps'.format(fn)
        if should_standardize_size:
            ThumbnailMod.MakeThumbSizeCanvasInFolder(thumb_size, steps_folder)
            print('{}: Step images resolution standardized'.format(fn))
        GifCreator.SaveToGif(fn, processedImgDirectory+'/{}'.format(fn), outputDirectory, extra_gif_frames)
        print('{}: GIF created'.format(fn))

if flag==False:
    print('No images found. Please copy images into the',baseImgDirectory,'folder.')

input('Program finished executing. Press any key to continue')