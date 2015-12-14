import SimpleCV
import sys
from pipeline import *

def load_data(filename):
    data = []
    image_names = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.split()
            data.append( ( SimpleCV.Image(parts[0]), (int(parts[1]), int(parts[2])) ) )
            image_names.append(parts[0])
    return data, image_names

if __name__ == '__main__':
    pipeline = Pipeline(filename=sys.argv[1])
    data, image_names = load_data(sys.argv[2])

    error = pipeline.error(data)
    performance = pipeline.performance([x[0] for x in data])

    print 'Error:', error
    print 'Performance:', performance

    #for i, (img, location) in enumerate(data):
    #    name = image_names[i]
    #    print name

    #    drawn_img = pipeline.draw(img)
    #    drawn_img.save(name + '.' + sys.argv[1] + '.jpg')
    #    drawn_img.show()
    #    raw_input()
    #    #pipeline.process(img).show()
    #    #raw_input()
