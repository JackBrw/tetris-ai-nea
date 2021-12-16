import numpy as np
array = np.array([[1, 0, 0, 0],
                  [2, 3, 0, 0],
                  [0, 4, 0, 0],
                  [0, 0, 0, 0]])

array = np.transpose(array)
array = np.flip(array, 1)

print(array)