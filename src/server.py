import numpy as np
import os
import sys
import json
from bottle import Bottle, run, template, request, static_file, abort
# from caffenet import CaffeNet, load_image_from_bytestream
from utils import load_config, load_image_from_bytestream

# Filter allowed extensions server-side
ALLOWED_EXTS = ['.png', '.jpg', '.jpeg']

# Load config variables
config = load_config('config.json')
HOSTNAME = config['HOSTNAME']
PORT = config['PORT']
DEPLOY_PROTOTXT_PATH = config['DEPLOY_PROTOTXT_PATH']
WEIGHTS_PATH = config['WEIGHTS_PATH']

# Initialize Caffe wrapper
# caffe_net = CaffeNet(DEPLOY_PROTOTXT_PATH, WEIGHTS_PATH)

# Use dummy CaffeNet
class DummyCaffeNet:

    def __init__(self, caffe_model_path, deploy_protoxt_path):
        pass

    def predict(self, image):
        p = np.random.rand()
        return [p, 1-p]

caffe_net = DummyCaffeNet(DEPLOY_PROTOTXT_PATH, WEIGHTS_PATH)

app = Bottle()

@app.route('/')
def sendIndex():
    return static_file('index.html', root='')

# Serve static files
@app.route('/<filename:path>')
def send_static(filename):
    return static_file(filename, root='')

# Process uploaded image. The request should have a file in the 'image' attribute.
@app.route('/upload', method='POST')
def submitImage():
    imageData = request.files.get('image')
    filename, ext = os.path.splitext(imageData.filename)
    if not ext in ALLOWED_EXTS:
        # Throw error
        abort(400, 'File type not supported')
    else:
        image = load_image_from_bytestream(imageData.file)
        result = caffe_net.predict(image)

        ret = {
            'confidences': result
        }
        return json.dumps(ret)

@app.error(400)
@app.error(500)
def handleError(error):
    ret = {
        '_status_code': error._status_code,
        '_status_line': error._status_line,
        'body': error.body,
        'traceback': error.traceback
    }
    return json.dumps(ret)

run(app, host=HOSTNAME, port=PORT)
