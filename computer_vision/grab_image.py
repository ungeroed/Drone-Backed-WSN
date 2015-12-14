import SimpleCV
import sys

if __name__ == '__main__':
    cam = SimpleCV.Camera()
    img = cam.getImage()
    img.save(sys.argv[1])
