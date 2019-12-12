from PIL import Image
import os
import math
import numpy as np
import random

# File contains palette operations on images

# ---------------------------------
# Internal functions
# ---------------------------------

# Clamps input value between two values
def clamp(val, minval, maxval):
    if val < minval: return minval
    if val > maxval: return maxval
    return val

# Custom loss function that takes minimum value 1 when col1 and col2 are equal
def SqrLoss(col1, col2):
    return (1/(1+((col1[0] - col2[0])*(col1[0] - col2[0]) + (col1[1] - col2[1])*(col1[1] - col2[1]) + (col1[2] - col2[2])*(col1[2] - col2[2]))))


# ---------------------------------
# External functions
# ---------------------------------
# Function returns a paletted version of an image, and a list of palette colours mapped to palette index
def ReduceToPalette(image, pal_count):
    result = image.convert('P', palette=Image.ADAPTIVE, colors = pal_count)
    imgPalList = result.getpalette()
    imgPalList = imgPalList[0:pal_count*3]
    palCols = list() 
    for i in range(pal_count):
        palColIter = (imgPalList[3*i],imgPalList[3*i+1], imgPalList[3*i+2])
        palCols.append(palColIter)
    return (result, palCols)

# Function returns an image consiting of palette colours
def MakePalImg(palList, scale):
    pal_count = len(palList)
    pal_img_dim = (int)(math.ceil((math.sqrt(pal_count))))
    palImg = Image.new(mode = 'RGB', size = (pal_img_dim, pal_img_dim))
    palPix = palImg.load()
    for i in range(pal_count):
        current_index = ((int)(i/pal_img_dim), i%pal_img_dim)
        palPix[current_index] = palList[i]
    palImg = palImg.resize(size = (pal_img_dim * scale, pal_img_dim * scale))
    return palImg

# Finds mean position of a particular colour in an image. Image must be paletted and palette index to colour map must be passed
def GetMeanOfColInImage(image,palList,col):
    pixMap = image.load()
    (width, height) = image.size
    totalCount = 0
    totalWeightX = 0
    totalWeightY = 0
    for i in range(width):
        for j in range(height):
            if (palList[pixMap[i,j]] == col):
                totalWeightX += i
                totalWeightY += j
                totalCount += 1
    
    if (totalCount == 0):
        totalCount = 1

    meanX = clamp(int(round(totalWeightX / totalCount)),0,image.size[0])
    meanY = clamp(int(round(totalWeightY / totalCount)),0,image.size[1])
    return (meanX, meanY)

# Draws a square box of specified size of a specific colour and specified middle point on an existing image
def DrawBox(srcimage, coords, boxSize, color):
    newImage = Image.new(mode = "RGB", size = (boxSize,boxSize), color = color)
    (oldWidth, oldHeight) = srcimage.size
    x1 = (int)((coords[0] - (boxSize / 2)))
    y1 = (int)((coords[1] - (boxSize / 2)))
    srcimage.paste(newImage, (x1,y1))
    return srcimage
