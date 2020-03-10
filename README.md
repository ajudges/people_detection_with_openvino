# People detection on the Edge

This solution is intended to be run on the edge and it detects the presence of people for certain actions to be carried out. It prints when people have been detected, together with the time when they are detected. It is meant to be run as an IoT solution for detecting people and activating events: such as the switching on of lights, opening doors etc. Hence it does not store nor display the images captured.

## Architecture
This solution makes use of a people's detection model which has been converted into intermediate representation files, so as to enable fast performance and optimization on all Intel processors. It prints 'None' when it does not detect anyone; 'Persons Detected" and timestamp (from video it gives the current position of the video in seconds) when it detects people. The input stream can either be from the camera of the device or an input video. The default confidence threshold to output the result is 0.5, adding the argument _-ct {desired-threshold}_ to the app.py


## Instructions

1. To capture from camera: On the terminal run

```
python app.py
```
2. To capture from a video: On the terminal run
```
python app.py -i {location-of-video}
```
3. To change the confidence threshold, include the argument -ct {desired-threshold} e.g.
```
python app.py -ct {0.6}
```

## Gratitude
A big thank you to Intel and Udacity, for the Intel Edge AI scholarship: which gave me the required tools to carry out this project. It has been an experience!

## Author
Nnamdi Ajah
