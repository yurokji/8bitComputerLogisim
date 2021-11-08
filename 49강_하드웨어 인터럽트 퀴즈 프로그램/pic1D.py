from PIL import Image
from itertools import chain
import numpy as np
import re
import array


def array2PIL(arr, size):
    mode = 'RGB'
    arr = arr.reshape(arr.shape[0]*arr.shape[1], arr.shape[2])
    if len(arr[0]) == 3:
        arr = np.c_[arr, 255*np.ones((len(arr),1), np.uint8)]
    return Image.frombuffer(mode, size, arr.tostring(), 'raw', mode, 0, 1)


def convColor24To16(color_in):
    rmax = 2**5 - 1
    gmax = 2**6 - 1
    bmax = 2**5 - 1
    r = int(round(color_in[0] * (rmax / 255)))
    g = int(round(color_in[1] * (gmax / 255)))
    b = int(round(color_in[2] * (bmax / 255)))
    color_out = r << 11
    color_out = color_out | (g << 5)
    color_out = color_out | b
    return color_out


im = Image.open("lionel-messi-2.jpg")
im.show()
# im = Image.fromarray(np.array(Image.open(imgName)).astype("uint16"))
print("Image mode: ",im.mode)
im2 = Image.new(im.mode, im.size)
pix = im.load()
width = im.size[0]
height = im.size[1]

fname = 'testpic.bin'
fp = open(fname, 'wb') 

# offset = 2048*10
# image = array.array('B', [0, 0] * (width * height  * size + offset) )
image = array.array('H', [0] * (width * height) )

count = 0
for i in range(width):
    for j in range(height):
        col_in = list(pix[j, i])
        image[count] = convColor24To16(col_in)
        count += 1

image.tofile(fp)
fp.close()
