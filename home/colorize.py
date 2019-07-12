import torch

import os
import colorgram.colorgram as cgm

import sys
import time
from PIL import Image
from torchvision import transforms
from preprocess import re_scale, save_image, make_colorgram_tensor, scale

from models import DeepUNetPaintGenerator
from utils import load_checkpoints

topk = 4


def get_rgb(colorgram_result):
    """
    from colorgram_result, result rgb value as tuple of (r,g,b)
    """
    color = colorgram_result.rgb
    return (color.r, color.g, color.b)


def crop_region(image):
    """
    from image, crop 4 region and return
    """
    width, height = image.size
    h1 = height // 4
    h2 = h1 + h1
    h3 = h2 + h1
    h4 = h3 + h1
    image1 = image.crop((0, 0, width, h1))
    image2 = image.crop((0, h1, width, h2))
    image3 = image.crop((0, h2, width, h3))
    image4 = image.crop((0, h3, width, h4))

    return (image1, image2, image3, image4)


def get_topk(color_info, k):
    colors = list(color_info.values())
    return list(map(lambda x: x[k], colors))


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# out_root = './data/colorize_result'
# if not os.path.exists(out_root):
#     os.mkdir(out_root)
generator = 'deepunetG_030.pth.tar'

model = DeepUNetPaintGenerator()
model = model.to(device)
load_checkpoints(generator, model, device_type=device.type)
for param in model.parameters():
    param.requires_grad = False


def act(stylefile,testfile):
    if len(sys.argv) < 3:
        raise RuntimeError(
            'Command Line Argument Must be (sketch file, style file)')

    style_f = stylefile
    # './data/styles/%s' % sys.argv[2]
    test_f = testfile
    # './data/test/%s' % sys.argv[1]

    filename = sys.argv[1][:-4] + sys.argv[2][:-4] + '.png'

    style = Image.open(style_f).convert('RGB')
    style = transforms.Resize((256, 256))(style)
    print(style)
    style_pil = style

    test = Image.open(test_f).convert('RGB')
    test_pil = transforms.Resize((256, 256))(test)

    transform = transforms.Compose(
        [transforms.Resize((256, 256)),
         transforms.ToTensor()])

    test = transform(test)
    test = scale(test)
    test = test.unsqueeze(0).to(device)

    to_pil = transforms.ToPILImage()
    nowtime = time.time()
    try:
        print(1)
        images = list(crop_region(style))
        print(images)
        result = {}
        for i, img in enumerate(images, 1):
            colors = cgm.extract(img, topk + 1)
            result[str(i)] = {
                '%d' % i: get_rgb(colors[i])
                for i in range(1, topk + 1)
            }
        nowtime2 = time.time()
        print(result)
        print(nowtime2-nowtime)
        color_tensor = make_colorgram_tensor(result)
        color_tensor = color_tensor.unsqueeze(0).to(device)

        fakeB, _ = model(test, color_tensor)
        fakeB = fakeB.squeeze(0)
        fakeB = re_scale(fakeB.detach().cpu())
        fakeB = to_pil(fakeB)
        fakeB.save(os.path.expanduser('media/result.jpg'))

        result_image = Image.new('RGB', (256 * 3, 256))
        result_image.paste(test_pil, (256 * 0, 0, 256 * 1, 256))
        result_image.paste(style_pil, (256 * 1, 0, 256 * 2, 256))
        result_image.paste(fakeB, (256 * 2, 0, 256 * 3, 256))
        result_image.save(os.path.expanduser('media/compareresult.jpg'))
        # save_image(result_image, os.path.join(out_root, filename))

    except IndexError:
        exit(1)
    nowtime2 = time.time()
    print(nowtime2-nowtime)

def actbycolor(stylelist,testfile):
    print(stylelist)
    print(stylelist[0])
    if len(sys.argv) < 3:
        raise RuntimeError(
            'Command Line Argument Must be (sketch file, style file)')
    result = {}
    j = 0
    for i in range(1,5):
        temp = {}
        for k in range(1,5):
            if j >= len(stylelist):
                j = 0
            temp[str(k)] = stylelist[j]
            j = j+1
        result[str(i)] = temp
    print(result)
    test_f = testfile

    # filename = sys.argv[1][:-4] + sys.argv[2][:-4] + '.png'
    test = Image.open(test_f).convert('RGB')
    test_pil = transforms.Resize((256, 256))(test)

    style = Image.open('media/immm.jpg').convert('RGB')
    style = transforms.Resize((256, 256))(style)
    print(style)
    style_pil = style

    transform = transforms.Compose(
        [transforms.Resize((256, 256)),
         transforms.ToTensor()])

    test = transform(test)
    test = scale(test)
    test = test.unsqueeze(0).to(device)

    to_pil = transforms.ToPILImage()
    nowtime = time.time()
    try:
        nowtime2 = time.time()
        print(result)
        print(nowtime2-nowtime)
        color_tensor = make_colorgram_tensor(result)
        color_tensor = color_tensor.unsqueeze(0).to(device)

        fakeB, _ = model(test, color_tensor)
        fakeB = fakeB.squeeze(0)
        fakeB = re_scale(fakeB.detach().cpu())
        fakeB = to_pil(fakeB)
        fakeB.save(os.path.expanduser('media/result.jpg'))

        result_image = Image.new('RGB', (256 * 3, 256))
        result_image.paste(test_pil, (256 * 0, 0, 256 * 1, 256))
        result_image.paste(style_pil, (256 * 1, 0, 256 * 2, 256))
        result_image.paste(fakeB, (256 * 2, 0, 256 * 3, 256))
        result_image.save(os.path.expanduser('media/compareresult.jpg'))
        # save_image(result_image, os.path.join(out_root, filename))

    except IndexError:
        exit(1)
    nowtime2 = time.time()
    print(nowtime2-nowtime)
# if __name__ == "__main__":
#     main()