import argparse
import cv2
import numpy as np
from inference import Network
from _ast import Break
from datetime import datetime

INPUT_STREAM = "videoplayback.mp4"
CPU_EXTENSION = "/opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so"

def get_args():
    '''
    Gets the arguments from the command line.
    '''
    parser = argparse.ArgumentParser("Get the location of an input video")
    # -- Description for the command
    i_desc = "The location of the input video"
    m_desc = "The location of people model XML file"
    #n_desc = "The location of violence model XML file"
    d_desc = "The device name, if not CPU"
    ct_desc = "The confidence threshold to use for output"
    
    # -- Add required and optional groups
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    
    # -- Create the argument
    required.add_argument("-m", help=m_desc, default='./model/person_model_88.xml',required = False)
    optional.add_argument("-i", help=i_desc, default=0) #default = 0 to read from camera
    optional.add_argument("-d", help=d_desc, default='CPU')
    optional.add_argument("-ct", help=ct_desc, default=0.5)
    args = parser.parse_args()
    
    return args




def inference_result(result, current_pos, args):
    '''
    Return when a person has been detected together with the time
    '''
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if args.i!=0:
        time = int((current_pos//1000)%60)
    for people in result[0][0]: # Output shape is 1x1x100x7
        conf = people[2]
        if conf >= args.ct:
            return "People detected", time



def capture_video(args):
    
    # Convert the args for confidence
    args.ct = float(args.ct)
    
    # initialize the inference engines for people and violence
    people_plugin = Network()
    violence_plugin = Network()
    
    # load the network models into the IE
    people_plugin.load_model(args.m, args.d, None)
        
    cap = cv2.VideoCapture(args.i)
    cap.open(args.i)
    
    # Grab the shape of the input 
    width = int(cap.get(3))
    height = int(cap.get(4))
    
    # Create a video writer for the output video
    # The second argument should be `cv2.VideoWriter_fourcc('M','J','P','G')`
    # on Mac, and `0x00000021` on Linux
    #video_code = cv2.VideoWriter_fourcc('M','J','P','G')
    #out = cv2.VideoWriter('out.mp4', video_code, 30, (width,height))
    
    while cap.isOpened():
        # Capture frame by frame
        flag, frame = cap.read()
        if not flag:
            break
        # cv2.imshow('Frame',frame)
        key_pressed = cv2.waitKey(60)
        
        #width and height of person detection model
        dsize = (544, 320)
        
        # get the current position of the video
        current_pos = cap.get(cv2.CAP_PROP_POS_MSEC)
        
        p_frame = cv2.resize(frame, dsize)
        p_frame = p_frame.transpose((2,0,1))
        p_frame = p_frame.reshape(1,3,320,544)
    
        # Perform inference on the frame
        people_plugin.async_inference(p_frame)
        
        ### Get the output of inference
        if people_plugin.wait() == 0:
            people_result = people_plugin.extract_output()
            
            
            ### Update the frame to include detected bounding boxes
            output = inference_result(people_result, current_pos, args)
            # Write out the frame
            print (output)
            
        
        # Break if escape key pressed
        if key_pressed == 27:
            break
            
    
    # Release the , capture, and destroy any OpenCV windows    
    
    cap.release()
    cv2.destroyAllWindows()

def main():
    args = get_args()
    capture_video(args)

if __name__ == "__main__":
    main()
