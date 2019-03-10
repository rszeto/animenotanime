import json

import numpy as np
import skimage
from PIL import Image

def load_config(path):
    # Load file as dictionary
    with open(path, 'r') as f:
        json_obj = json.load(f)

    # Convert keys and values from unicode to str
    ret = {}
    for key, value in json_obj.iteritems():
        if isinstance(key, unicode):
            key = str(key)
        if isinstance(value, unicode):
            value = str(value)
        ret[key] = value
    return ret

'''
Given the bytestream for the image, returns a NumPy float32 array with shape (H x W x 3).
Grayscale images are converted to color, and alpha channel is removed. 
'''
def load_image_from_bytestream(stream):
    # Load image from stream
    pil_image = Image.open(stream)
    # Convert image to NumPy float32 array, as expected for CaffeNet
    img = skimage.img_as_float(pil_image).astype(np.float32)
    # Convert grayscale images to color
    if img.ndim == 2:
        img = img[:, :, np.newaxis]
        img = np.tile(img, (1, 1, 3))
    # Remove alpha channel is present
    elif img.shape[2] == 4:
        img = img[:, :, :3]
    return img