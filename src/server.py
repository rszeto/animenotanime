import json
import os
import sys
import traceback

import numpy as np
from flask import Flask, render_template, request

from utils import load_image_from_bytestream

# Filter allowed extensions server-side
ALLOWED_EXTS = ['.png', '.jpg', '.jpeg']

# Use dummy CaffeNet
class DummyCaffeNet(object):

    def predict(self, image):
        p = np.random.rand()
        return [p, 1-p]

caffe_net = DummyCaffeNet()

app = Flask(__name__)

@app.route('/')
def sendIndex():
    return render_template('index.html')

# Process uploaded image. The request should have a file in the 'image' attribute.
@app.route('/upload', methods=['POST'])
def submitImage():
    imageData = request.files.get('image')
    filename, ext = os.path.splitext(imageData.filename)
    if not ext in ALLOWED_EXTS:
        # Throw error
        abort(400, 'File type not supported')
    else:
        image = load_image_from_bytestream(imageData.stream)
        result = caffe_net.predict(image)

        ret = {
            'confidences': result
        }
        return json.dumps(ret)

@app.errorhandler(400)
@app.errorhandler(500)
def handleError(error):
    stack_trace = traceback.format_exc()
    error_message = error.message

    ret = {
        'body': stack_trace,
        'traceback': stack_trace
    }

    return json.dumps(ret)
