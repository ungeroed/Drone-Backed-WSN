from math import *
import matplotlib.pyplot as plt

if __name__ == '__main__':
    e = 0.00317
    f = lambda a: e * sqrt( (1.008*a)**2 + (0.776*a)**2 )

    data = map(f, range(161))
    plt.ylabel('Accuracy (cm)')
    plt.xlabel('Altitude (cm)')
    plt.grid(True)
    plt.plot(data)
    plt.show()

    raw_input()
