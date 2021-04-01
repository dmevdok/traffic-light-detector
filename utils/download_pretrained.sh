#!/bin/bash

mkdir pretrained

curl -L https://www.dropbox.com/s/hbw9u3k51sf492w/signal_classifier.pt?dl=0 --output pretrained/signal_classifier.pt 
curl -L https://www.dropbox.com/s/76mz2xpl1syo43b/traffic_light_detector.pt?dl=0 --output pretrained/traffic_light_detector.pt 
