import os
from instabot import Bot
from dotenv import load_dotenv
import os.path
import tempfile
from instabot.api.api_photo import compatible_aspect_ratio, get_image_size
import numpy as np
import PIL.Image
from scipy.optimize import minimize_scalar


def post_photos():
    pics = os.listdir('images/')
    pics = ['images/{}'.format(x) for x in pics]
    load_dotenv()
    login = os.getenv("LOGIN")
    password = os.getenv('PASSWORD')
    bot = Bot()
    bot.login(username=login, password=password)
    for photo in pics:
        bot.upload_photo(fix_photo(photo))


def correct_ratio(photo):
    return compatible_aspect_ratio(get_image_size(photo))

def strip_exif(img):
    """Strip EXIF data from the photo to avoid a 500 error."""
    data = list(img.getdata())
    image_without_exif = PIL.Image.new(img.mode, img.size)
    image_without_exif.putdata(data)
    return image_without_exif


def fix_photo(photo):
    with open(photo, 'rb') as f:
        img = PIL.Image.open(f)
        img = strip_exif(img)
        if not correct_ratio(photo):
            img = get_highest_entropy(img)
        photo = os.path.join(tempfile.gettempdir(), 'instacron.jpg')
        img.save(photo)
    return photo


def entropy(data):
    """Calculate the entropy of an image"""
    hist = np.array(PIL.Image.fromarray(data).histogram())
    hist = hist / hist.sum()
    hist = hist[hist != 0]
    return -np.sum(hist * np.log2(hist))


def crop(x, y, data, w, h):
    x = int(x)
    y = int(y)
    return data[y:y + h, x:x + w]


def get_highest_entropy(img, min_ratio=4 / 5, max_ratio=90 / 47):
    w, h = img.size
    data = np.array(img)
    ratio = w / h
    if ratio > max_ratio:
        # Too wide
        w_max = int(max_ratio * h)

        def _crop(x): return crop(x, y=0, data=data, w=w_max, h=h)
        xy_max = w - w_max
    else:
        # Too narrow
        h_max = int(w / min_ratio)

        def _crop(y): return crop(x=0, y=y, data=data, w=w, h=h_max)
        xy_max = h - h_max
    x = minimize_scalar(lambda xy: -entropy(_crop(xy)),
                        bounds=(0, xy_max),
                        method='bounded').x
    return PIL.Image.fromarray(_crop(x))