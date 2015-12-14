import SimpleCV
from pipeline import *
import sys

if __name__ == '__main__':
    pipeline = Pipeline(filename=sys.argv[1])
    for p in pipeline.processors:
        print p

    cam = SimpleCV.Camera()
    while True:
        img = cam.getImage()
        img = pipeline.process(img)
        img = pipeline.draw(img)
        img.show()
