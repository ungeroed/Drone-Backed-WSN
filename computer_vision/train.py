import SimpleCV
import sys
from pipeline import *

def load_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.split()
            data.append( ( SimpleCV.Image(parts[0]), (int(parts[1]), int(parts[2])) ) )
    return data

if __name__ == '__main__':
    # Load the training data
    imgs = load_data(sys.argv[1])

    # Construct and train the pipeline 
    #pipeline = Pipeline(processors=[
    #    	HueDistanceProcessor(165),
    #    	ThresholdProcessor(40),
    #    	#InvertProcessor(),
    #    	ErodeProcessor(5),
    #])
    #trained_pipeline = pipeline.train(imgs)

    pipeline = Pipeline()
    trained_pipeline = pipeline.evolve(imgs)

    trained_pipeline.save(sys.argv[2])
