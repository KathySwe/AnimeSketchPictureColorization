
from __future__ import print_function
import os
import sys
from PIL import Image

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def create_colorimg(a,b,c,d):
    print(a)
    img = Image.new('RGB', (512, 128), color = a)
    img.save('p1.png')

    img = Image.new('RGB', (512, 128), color = b)
    img.save('p2.png')

    #img = Image.new('RGB', (60, 30), color = (155, 50, 20))
    img = Image.new('RGB', (512, 128), color = c)
    img.save('p3.png')

    img = Image.new('RGB', (512, 128), color = d)
    img.save('p4.png')
    files = [
        'p1.png',
        'p2.png',
        'p3.png',
        'p4.png',
        ]

    result = Image.new("RGB", (512,512))


    path = os.path.expanduser(files[0])
    img = Image.open(path)
    # img.thumbnail((50,50), Image.ANTIALIAS)
    x = 0
    y =0
    w, h = img.size
    print('pos {0},{1} size {2},{3}'.format(x, y, w, h))

    result.paste(img, (x, y, x + w, y + h))
    path = os.path.expanduser(files[1])
    img = Image.open(path)
    # img.thumbnail((50,50), Image.ANTIALIAS)
    x = 0
    y = 128
    w, h = img.size
    print('pos {0},{1} size {2},{3}'.format(x, y, w, h))

    result.paste(img, (x, y, x + w, y + h))
    path = os.path.expanduser(files[2])
    img = Image.open(path)
    # img.thumbnail((50,50), Image.ANTIALIAS) 
    x = 0
    y = 256
    w, h = img.size
    print('pos {0},{1} size {2},{3}'.format(x, y, w, h))

    result.paste(img, (x, y, x + w, y + h))
    path = os.path.expanduser(files[3])
    img = Image.open(path)
    # img.thumbnail((50,50), Image.ANTIALIAS) 
    x = 0
    y = 384
    w, h = img.size
    print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
    result.paste(img, (x, y, x + w, y + h))

    result=result.transpose(Image.ROTATE_90)
    a=result.save(os.path.expanduser('media/immm.jpg'))
    
    
    return result

print(hex_to_rgb('#ff1b1b'))
