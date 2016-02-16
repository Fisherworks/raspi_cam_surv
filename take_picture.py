#! /usr/bin/env python
import time, argparse, sys, os
import datetime as dt
import picamera

def takePicture(fileName='raspicam.jpg', picQuality='low'):
    # Explicitly open a new file called my_image.jpg
    # print fileName
    my_file = open(fileName, 'wb')
    with picamera.PiCamera() as camera:
        camera.led = False
        camera.sharpness = 50
        camera.meter_mode = 'backlit'
        camera.exposure_compensation = 10
        if picQuality != 'low':
            camera.resolution = (2592, 1944)
            camera.annotate_text_size = 64
        else:
            camera.resolution = (640, 480)
            camera.annotate_text_size = 16
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        camera.start_preview()
        time.sleep(2)
        camera.capture(my_file)
    # At this point my_file.flush() has been called, but the file has
    # not yet been closed
    my_file.close()
    return fileName

def main(argv):
    # ======arguments parser ==========#

    parser = argparse.ArgumentParser(description='control RasPi to take picture with highest resolution.')
    parser.add_argument('-c', '--count', help='total count of pics should be taken', type=int, required=True)
    parser.add_argument('-t', '--timespan', help='the time span between 2 or more pics, 3 seconds at least', type=int, required=True)
    args = parser.parse_args()

    count = args.count 
    timeSpan = args.timespan
    timeSpan = timeSpan - 3 if timeSpan >= 3 else 0
    timeSpan = 0 if count == 1 else timeSpan
    
    picDir = os.path.dirname(os.path.abspath(__file__))
    picDir = os.path.join(picDir, 'static/')

    while count:
        fileName = picDir + 'raspicam_' + dt.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'
        takePicture(fileName, 'high')
        count -= 1
        if count:
            time.sleep(timeSpan)
    
    return fileName
    
if __name__ == "__main__":
    main(sys.argv[1:])

