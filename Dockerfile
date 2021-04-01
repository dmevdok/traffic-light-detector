FROM pytorch/pytorch

RUN apt -y update && apt -y install ffmpeg && pip install ffmpeg-python

COPY yolo_requirements.txt /yolo_requirements.txt

RUN yes | pip install opencv-python torchvision && pip install -r /yolo_requirements.txt && apt -y install curl

RUN mkdir -p /root/.cache/torch/hub && curl https://github.com/ultralytics/yolov5/archive/master.zip --output /root/.cache/torch/hub/master.zip

ADD pretrained /pretrained

COPY test.py /test.py

WORKDIR /

ENTRYPOINT ["python", "test.py"]