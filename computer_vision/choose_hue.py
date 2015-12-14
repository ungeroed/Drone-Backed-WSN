import SimpleCV
import sys
from pipeline import *

if __name__ == '__main__':
	img = SimpleCV.Image(sys.argv[1])

	for hue in range(0, 256, 5):
		pipeline = Pipeline(processors=[
			HueDistanceProcessor(hue),
			ThresholdProcessor(40),
			ErodeProcessor(5),
		])
		print hue
		pipeline.process(img).show()
		raw_input()
