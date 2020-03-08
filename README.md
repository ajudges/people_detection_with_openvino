# People detection 

This solution is intended to be run on the edge and it detects the presence of people for certain actions to be carried out. It prints when people have been detected, together with the time (in seconds) when they are detected.

## Architecture
This solution makes use of a people's detection model which has been converted into intermediate representation files, so as to enable it to be used on Intel processors. It prints 'None' when it does not detect anyone; 'Persons Detected" and time (in seconds) when it detects people. The default confidence threshold to output the result is 0.5, adding the argument _-ct {desired-threshold}_ to the app.py


## Instructions

From terminal/command line, run

```
python app.py -i {location-of-video}
```

## Gratitude
A big thank you to Intel and Udacity, for the Intel Edge AI scholarship: which gave me the required tools to carry out this project. It has been an experience!

## Author
Nnamdi Ajah
