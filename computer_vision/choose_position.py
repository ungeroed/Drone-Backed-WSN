import SimpleCV
import sys

if __name__ == '__main__':
    for path in sys.argv[1:]:
		img = SimpleCV.Image(path)
		disp = SimpleCV.Display()

		while disp.isNotDone():
			img.save(disp)
			if disp.mouseLeft:
				print path, disp.mouseX, disp.mouseY
				break
			if disp.mouseRight:
				print path, -1, -1
				break
