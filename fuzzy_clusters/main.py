import numpy as np
import Fuzz
from matplotlib import pyplot as plt

def main():
    feature_num = 0
    data = []
    with open('sample1.csv') as data_file:
        header = data_file.readline()
        feature_num = len(header.split(','))
        for line in data_file:
            data.append(line.split(','))
    data = np.asarray(data, np.float64)
    fcm = Fuzz.FCM(4)
    fcm.fit(data)

    fcm_centers = fcm.centers
    fcm_labels  = fcm.u.argmax(axis=1)
    f, axes = plt.subplots(1, 1)
    plt.scatter(data[:,0], data[:,1])
    plt.scatter(data[:,0], data[:,1])
    plt.scatter(fcm_centers[:,0], fcm_centers[:,1])
    plt.show()

if __name__ == '__main__':
    main()
