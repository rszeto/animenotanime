import numpy as np
import sys
import skimage
from PIL import Image
from utils import load_config

# Load config variables
config = load_config('config.json')
PYCAFFE_PATH = config['PYCAFFE_PATH']

# Import Caffe
sys.path.append(PYCAFFE_PATH)
import caffe

class CaffeNet:
    __IMAGENET_MEAN = np.array([104.0, 116.67, 122.68])

    def __init__(self, caffe_model_path, deploy_protoxt_path):
        self.net = caffe.Net(caffe_model_path, deploy_protoxt_path, caffe.TEST)
        self.transformer = caffe.io.Transformer({'data': self.net.blobs['data'].data.shape})
        self.transformer.set_transpose('data', (2, 0, 1))  # height*width*channel -> channel*height*width
        self.transformer.set_mean('data', CaffeNet.__IMAGENET_MEAN)  #### subtract mean ####
        self.transformer.set_raw_scale('data', 255)  # pixel value range
        self.transformer.set_channel_swap('data', (2, 1, 0))  # RGB -> BGR

    def predict(self, image):
        self.net.blobs['data'].data[...] = self.transformer.preprocess('data', image)
        out = self.net.forward()
        # Extract and return probabilities
        return out['prob'].flatten().tolist()

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