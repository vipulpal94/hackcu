import math
import sys
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib

def load_mnist_training_data (filename):
    label_file = open(filename, 'rb')

    magic_number = int.from_bytes(label_file.read(4), byteorder='big')
    if magic_number != 0x00000803:
        print('Invalid MNIST training label file')
        sys.exit(-1)

    number_of_images = min(10000, int.from_bytes(label_file.read(4), byteorder='big'))
    number_of_rows = int.from_bytes(label_file.read(4), byteorder='big')
    number_of_columns = int.from_bytes(label_file.read(4), byteorder='big')

    images = []
    for image in range(number_of_images):
        if image % 1000 == 0:
            print('Loading Image #' + str(image))
        image = []
        for row in range(number_of_rows):
            for column in range(number_of_columns):
                pixel = int.from_bytes(label_file.read(1), byteorder='big')
                image.append(pixel)

        images.append(image)

    return images


def load_mnist_training_labels (filename):
    label_file = open(filename, 'rb')

    magic_number = int.from_bytes(label_file.read(4), byteorder='big')
    if magic_number != 0x00000801:
        print('Invalid MNIST training label file')
        sys.exit(-1)

    number_of_labels = min(10000, int.from_bytes(label_file.read(4), byteorder='big'))

    labels = []
    for i in range(number_of_labels):
        label = int.from_bytes(label_file.read(1), byteorder='big')
        labels.append(label)

    return labels


def main (argv):
    filename = 'data/train-labels-idx1-ubyte'
    training_labels = load_mnist_training_labels(filename)

    filename = 'data/train-images-idx3-ubyte'
    training_data = load_mnist_training_data(filename)
    
    clf = MLPClassifier(solver='sgd', verbose=True, alpha=1e-6, hidden_layer_sizes=(10000, 10), random_state=1, activation='tanh')
    clf.fit(training_data, training_labels)  

    filename = 'test/t10k-labels-idx1-ubyte'
    testing_labels = load_mnist_training_labels(filename)

    filename = 'test/t10k-images-idx3-ubyte'
    testing_data = load_mnist_training_data(filename)

    accuracy = clf.score(testing_data, testing_labels)
    print(accuracy*100)

    joblib.dump(clf, 'hmm.pkl')


if __name__ == '__main__':
    main(sys.argv)
