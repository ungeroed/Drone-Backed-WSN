import SimpleCV, numpy, copy, pickle, time, math, random

class Processor():

    def process(self, img):
        '''
        Process the given image

        img: image
        returns: image
        '''
        raise Exception("Function must be overridden")

    def neighbors(self):
        '''
        Returns the neighboring states of the processor
        '''
        raise Exception("Function must be overridden")

    def mutate(self):
        '''
        Returns the a single neighboring state of the processor
        '''
        ns = self.neighbors()
        if len(ns) == 0:
            return self
        else:
            return random.choice(ns)

class ToHSVProcessor(Processor):
    def process(self, img):
        return img.toHSV()
    def neighbors(self):
        return []

class ToGrayProcessor(Processor):
    def process(self, img):
        return img.toGray()
    def neighbors(self):
        return []

class ToRGBProcessor(Processor):
    def process(self, img):
        return img.toRGB()
    def neighbors(self):
        return []

class ToBGRProcessor(Processor):
    def process(self, img):
        return img.toBGR()
    def neighbors(self):
        return []

class ChannelSelectionProcessor(Processor):
    def __init__(self, channel=0):
        self.channel = channel 
    def process(self, img):
        return img.splitChannels()[self.channel]
    def neighbors(self):
        return [ChannelSelectionProcessor(x) for x in [1, 2, 3] if x != self.channel]

class HistogramEqualizationProcessor(Processor):
    def process(self, img):
        return img.equalize()
    def neighbors(self):
        return []

class ThresholdProcessor(Processor):
    def __init__(self, threshold=150):
        self.threshold = threshold 
    def process(self, img):
        return img.binarize(self.threshold)
    def neighbors(self):
        n = []
        if self.threshold > 0:
            n.append(ThresholdProcessor(self.threshold-1))
        if self.threshold < 255:
            n.append(ThresholdProcessor(self.threshold+1))
        return n

class HueDistanceProcessor(Processor):
    def __init__(self, hue=150):
        self.hue = hue
    def process(self, img):
        return img.hueDistance(self.hue)
    def neighbors(self):
        n = []
        if self.hue > 0:
            n.append(HueDistanceProcessor(self.hue-1))
        if self.hue < 255:
            n.append(HueDistanceProcessor(self.hue+1))
        return n

class InvertProcessor(Processor):
    def process(self, img):
        return img.invert()
    def neighbors(self):
        return []

class MedianFilterProcessor(Processor):
    def __init__(self, window_size=5):
        self.window_size = window_size 
    def process(self, img):
        return img.medianFilter(self.window_size)
    def neighbors(self):
        n = []
        if self.window_size >= 5:
            n.append(MedianFilterProcessor(self.window_size-2))
        n.append(MedianFilterProcessor(self.window_size+2))
        return n

class BilateralFilterProcessor(Processor):
    def __init__(self, window_size=5):
        self.window_size = window_size 
    def process(self, img):
        return img.bilateralFilter(self.window_size)
    def neighbors(self):
        n = []
        if self.window_size >= 5:
            n.append(BilateralFilterProcessor(self.window_size-2))
        n.append(BilateralFilterProcessor(self.window_size+2))
        return n

class DilateProcessor(Processor):
    def __init__(self, iterations=3):
        self.iterations = iterations 
    def process(self, img):
        return img.dilate(self.iterations)
    def neighbors(self):
        n = []
        if self.iterations >= 2:
            n.append(DilateProcessor(self.iterations-1))
        n.append(DilateProcessor(self.iterations+1))
        return n

class ErodeProcessor(Processor):
    def __init__(self, iterations=3):
        self.iterations = iterations 
    def process(self, img):
        return img.erode(self.iterations)
    def neighbors(self):
        n = []
        if self.iterations >= 2:
            n.append(DilateProcessor(self.iterations-1))
        n.append(DilateProcessor(self.iterations+1))
        return n

class OpenProcessor(Processor):
    def process(self, img):
        return img.morphOpen()
    def neighbors(self):
        return []

class CloseProcessor(Processor):
    def process(self, img):
        return img.morphClose()
    def neighbors(self):
        return []

class EdgeDetectionProcessor(Processor):
    def process(self, img):
        return img.edges()
    def neighbors(self):
        return []


class Pipeline():

    def __init__(self, processors = [], filename = None):
        self.processors = processors

        self.processor_initializers = [
            ToHSVProcessor,
            ToGrayProcessor,
            ToRGBProcessor,
            ToBGRProcessor,
            ChannelSelectionProcessor,
            HistogramEqualizationProcessor,
            ThresholdProcessor,
            InvertProcessor,
            #BilateralFilterProcessor,
            MedianFilterProcessor,
            DilateProcessor,
            ErodeProcessor,
            OpenProcessor,
            CloseProcessor,
            #EdgeDetectionProcessor
        ]

        if filename is not None:
            with open(filename, "r") as f:
                self.processors = pickle.load(f).processors

    def save(self, filename):
        with open(filename, "w") as f:
            pickle.dump(self, f)

    def process(self, img):
        '''
        Process the given image

        img: Image
        returns: Image 
        '''
        return reduce(lambda i, p: p.process(i), self.processors, img)

    def detect_object(self, processed_img):
        '''
        Detect the object on the given processed image

        processed_img: Image
        returns: location
        '''
        blobs = processed_img.findBlobs()

        print blobs

        if blobs is None:
            return (-1, -1)

        blobs = map(lambda x: (x.area(), x.centroid()), blobs)
        blobs = filter(lambda x: x[0] > 250, blobs)
        blobs = sorted(blobs, reverse=True)
        if len(blobs) == 0:
            return (-1, -1)
        else:
            return blobs[0][1]

    def neighbors(self):
        '''
        Compute and return all neighboring states of the pipeline

        returns: Pipeline list
        '''
        ns = [self]

        for i in range(len(self.processors)):
            p = self.processors[i]
            for n in p.neighbors():
                new_processors = [x for x in self.processors]
                new_processors[i] = n
                ns.append(Pipeline(new_processors))

        return ns

    def error(self, imgs):
        '''
        Compute the error of the pipeline on the given supervised training set
        of image/location pairs. A pair of (-1, -1) means that the object is
        not on the image

        imgs: (Image * (int * int)) list
        returns: float * float * float
        '''
        # Get a normalization factor, which is multiplied on all errors
        # Assumes that the images have the same size 
        norm_factor = 1.0 / numpy.linalg.norm( numpy.array(imgs[0][0].size()) )
        errors = []

        try:
            for img, expected_location in imgs:
                actual_location = self.detect_object(self.process(img))

                # No object, and no object found
                if expected_location[0] < 0 and actual_location[0] < 0:
                    errors.append(0.0)
                    continue

                # No object, but object found
                if expected_location[0] < 0 and actual_location[0] >= 0:
                    errors.append(1.0)
                    continue

                # Object, but no object found
                if expected_location[0] >= 0 and actual_location[0] < 0:
                    errors.append(1.0)
                    continue

                # Actual object found
                err_vector = numpy.array(expected_location) - numpy.array(actual_location)
                err_vector_length = numpy.linalg.norm(err_vector)
                img_err = err_vector_length * norm_factor

                errors.append(img_err)

            # avg, min, max
            return sum(errors) / float(len(errors)), min(errors), max(errors)
        except:
            return 9999999999999.0, 9999999999999.0, 9999999999999.0

    def performance(self, imgs):
        '''
        Compute the performance of the pipeline on the given images

        imgs: Image list
        returns: float * float * float
        '''
        milliseconds = lambda: int(round(time.time() * 1000))

        times = []

        for img in imgs:
            try:
                start_time = milliseconds() 
                x = self.detect_object(self.process(img))
                times.append(milliseconds() - start_time)
            except:
                pass

        # avg, min, max
        return sum(times) / float(len(times)), min(times), max(times)

    def draw(self, img):
        '''
        Draws the object location on the given image

        img: Image
        returns: Image
        '''
        img2 = img.copy()
        detected_location = self.detect_object(self.process(img2))
        
        if detected_location[0] >= 0:
            drawing_layer = SimpleCV.DrawingLayer(img.size())
            drawing_layer.circle(map(int, detected_location), 10, filled=True, color=SimpleCV.Color.BLUE)
            img2.addDrawingLayer(drawing_layer)
            img2.applyLayers()

        return img2

    def train(self, imgs):
        '''
        Train the pipeline on the given set of images, consisting of images and
        the location of objects on the images (supervised data set)

        imgs: (Image * (int * int)) list
        returns: Pipeline
        '''
        # Initially, the current pipeline is the only candidate
        selected = self
        error = 9999999999
        iteration = 0

        # Helper function for time measurement
        milliseconds = lambda: int(round(time.time() * 1000))

        while True:
            start_time = milliseconds() 

            candidates = selected.neighbors()
            candidates_with_errors = sorted(map(lambda c: ( c.error(imgs)[0], c), candidates))
            new_error = candidates_with_errors[0][0]

            # Print progress
            duration = milliseconds() - start_time
            print '%d: error = %f, time = %d ms' % (iteration, new_error, duration)
            iteration += 1
            if new_error >= error:
                return selected

            error = new_error
            selected = candidates_with_errors[0][1]

    def mutate(self):
        '''
        Mutate the pipeline, returning a new pipeline

        returns: Pipeline
        '''
        new_processors = map(copy.deepcopy, self.processors)

        # Mutate
        for processor in new_processors:
            if random.random() < (1.0 / float(len(new_processors))):
                processor.mutate()

        # Add
        while random.random() < (1.0 / (float(len(new_processors)+0.01))) and len(new_processors) < 10:
            new_processors.insert( 
                random.randint(0, len(new_processors)), 
                random.choice(self.processor_initializers)()
            )

        # Remove
        for processor in new_processors:
            if random.random() < (1.0 / float(len(new_processors))):
                new_processors.remove(processor)

        return Pipeline(new_processors)

    def crossover(self, other):
        '''
        Create a crossover pipeline / a mix between the current and given pipelines

        other: Pipeline
        returns: Pipeline
        '''
        part1 = self.processors[:random.randint(0, len(self.processors))]
        part2 = other.processors[random.randint(0, len(other.processors)):]

        new_length = len(part1) + len(part1)
        if new_length > 10:
            part2 = part2[new_length-10:]

        return Pipeline(map(copy.deepcopy, part1 + part2))

    def evolve(self, imgs, selected_pairs=2, crossovers_per_pair=3, mutations_per_selected=3, iterations=500):
        '''
        Evolve (train) the pipeline on the given set of images, consisting of
        images and the location of objects on the images (supervised data set)

        imgs: (Image * (int * int)) list
        selected_pairs: int
        crossovers_per_pair: int
        mutations_per_selected: int
        returns: Pipeline
        '''
        # Initially, the current pipeline is the only candidate
        selected = [self]

        # Helper function for time measurement
        milliseconds = lambda: int(round(time.time() * 1000))

        for iteration in range(iterations):
            start_time = milliseconds() 

            candidates = [x for x in selected]

            # Generate crossovers
            if len(selected) > 1:
                for i in range(0, len(selected), 2):
                    a, b = selected[i:i+2]
                    for j in range(crossovers_per_pair):
                        candidates.append(a.crossover(b).mutate())

            # Generate mutation of previous round
            for s in selected:
                for j in range(mutations_per_selected):
                    candidates.append(s.mutate())

            # Compute the fitness of the candidates
            candidates_with_fitness = map(lambda c: ( c.error(imgs)[0], c), candidates)

            # Select the top candidates
            selected = map(lambda x: x[1], sorted(candidates_with_fitness)[:selected_pairs*2])

            # Print progress
            duration = milliseconds() - start_time
            print '%d: fitness = %f, time = %d ms' % (iteration, candidates_with_fitness[0][0], duration)

        return selected[0]
