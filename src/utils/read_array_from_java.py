import numpy as np


def read_array(input, dimensions):
    array = np.fromfile(input, dtype='>f4')
    return reshape_array(array, dimensions)


def reshape_array(array, dimensions):
    size = array.shape[0]
    cols = dimensions
    rows = size / dimensions
    array = array.reshape((rows, cols))
    return np.matrix(array)

