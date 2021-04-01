import torch
from torch.nn import functional as F
import ffmpeg
import PIL
import numpy as np
import torchvision
from tqdm.notebook import tqdm
import json
import sys

PREFIX = "."
OBJECT_DETECTION_MODEL = f'{PREFIX}/pretrained/yolov5s.pt'
CLASSIFICATION_MODEL = f'{PREFIX}/pretrained/signal_classifier.torch'
if torch.cuda.is_available():
    DEVICE = torch.device('cuda')
else:
    DEVICE = torch.device('cpu')
FRAME_SKIPPING = 2
VIDEO_PATH = sys.argv[-1]
VIDEO_WIDTH = 640

class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = torch.nn.Conv2d(in_channels=3, out_channels=6, kernel_size=3, stride=1, padding=0)
        self.pool1 = torch.nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        self.fc1 = torch.nn.Linear(630, 64)
        self.fc2 = torch.nn.Linear(64, 4)
    
    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.pool1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.log_softmax(x, 1)
        return x

def main():
    def classify(image, bboxes, coord_coef):
        def coord_transform(c):
            return int(c*coord_coef)
        frame_results = {}
        for tid, bbox in enumerate(bboxes):
            traffic_light = torch.unsqueeze(torch.tensor(image[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2]), :], dtype=torch.float32).permute(2,0,1), 0)
            tl_classify = torchvision.transforms.functional.resize(traffic_light.to(DEVICE), size=(32,16))
            prediction = torch.argmax(tlclassifier(tl_classify)[0]).item()
            frame_results[str(tid)] = {
                "coords": list(map(coord_transform,bbox[:-2])),
                "state": ['red','yellow','green','unknown'][prediction],
                "affect": True
            }
        return frame_results

    model = torch.hub.load(f'{PREFIX}/yolov5', 'custom', source="local", path_or_model=OBJECT_DETECTION_MODEL)

    tlclassifier = torch.load(CLASSIFICATION_MODEL)

    if torch.cuda.is_available():
        model.cuda()
        tlclassifier.cuda()
    else:
        model.cpu()
        tlclassifier.cpu()

    video_file = f"{PREFIX}/{VIDEO_PATH}"
    probe = ffmpeg.probe(video_file)
    video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    old_width = int(video_info['width'])
    old_height = int(video_info['height'])
    num_frames = int(eval(video_info['duration'])*eval(video_info['avg_frame_rate']))

    new_width = VIDEO_WIDTH
    new_height = int(old_height / (old_width / new_width))

    coord_coef = old_width / new_width

    frame_size = new_width*new_height*3
    process = (
        ffmpeg
        .input(video_file)
        .filter('scale', new_width, new_height)
        .output('pipe:', format='rawvideo', pix_fmt='rgb24')
        .run_async(pipe_stdout=True)
    )

    results = {}

    for j in range(num_frames):
        if j%FRAME_SKIPPING==0:
            frame = (
                np
                .frombuffer(process.stdout.read(frame_size), np.uint8)
                .reshape((new_height, new_width, 3))
            )
            prediction = model([frame]).xyxy[0]
            predicted_traffic_lights = prediction[prediction[:,5] == 9].cpu().numpy()
            if len(predicted_traffic_lights) > 0:
                results[str(j)] = classify(frame, predicted_traffic_lights, coord_coef)
                results[str(j+1)] = classify(frame, predicted_traffic_lights, coord_coef)

    json.dump(results, open(f"{VIDEO_PATH}.json","w"))

if __name__ == "__main__":
    main()