import json
import os
import sys
import traceback

import numpy as np
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from flask import Flask, render_template, request
from PIL import Image
from torch.nn.functional import softmax

# Filter allowed extensions server-side
ALLOWED_EXTS = ['.png', '.jpg', '.jpeg']

# Define and load prediction network from checkpoint
model = models.resnet18()
checkpoint = torch.load('model_best.pth.tar', map_location={'cuda:0': 'cpu'})
model.load_state_dict(checkpoint['state_dict'])

# Move network to CPU/GPU
device = torch.device('cuda', 0) if torch.cuda.is_available() else torch.device('cpu')
model.to(device)

# Set network to inference mode
model.eval()

# Define transform used on all input images for inference
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

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
        image = Image.open(imageData.stream).convert('RGB')
        image_tensor = transform(image).unsqueeze(0)
        output = model(image_tensor.to(device))
        confidences = softmax(output[0, :2]).detach().cpu().numpy().tolist()
        ret = dict(confidences=confidences)
        return json.dumps(ret)

@app.errorhandler(400)
@app.errorhandler(500)
def handleError(error):
    stack_trace = traceback.format_exc()

    ret = {
        'body': stack_trace,
        'traceback': stack_trace
    }

    return json.dumps(ret)
