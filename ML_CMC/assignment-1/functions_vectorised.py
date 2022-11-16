import numpy as np
def sum_non_neg_diag(X):
    Y = np.diag(X)
    u = np.where(Y < 0)
    Y[np.where(Y >= 0)[0]].sum()
    return -1 if len(u[0]) == len(Y) else Y[np.where(Y >= 0)[0]].sum()

def are_multisets_equal(x, y):
    x = np.array(x)
    y = np.array(y)
    x = np.sort(x)
    y = np.sort(y)
    return True if sum(x-y) == 0 else False

def max_prod_mod_3(x):
    Z = x[:-1] * x[1:]
    p = Z[np.where(Z % 3 == 0 )]
    return int(-1 if p.size == 0 else max(p))


def convert_image(image, weights):
    i = np.transpose(weights)
    x = image.ravel().reshape(-1, len(weights))
    o = np.reshape(np.sum((x * i).T, axis = 0), (len(image),-1))
    return o

def rle_scalar(x, y):
    x = np.transpose(x)
    x = np.repeat(x[0], x[1])
    y = np.transpose(y)
    y = np.repeat(y[0], y[1])
    return -1 if len(x) != len(y) else int(np.dot(x, y))
    
from scipy.spatial.distance import cdist
def cosine_distance(x,y):
    x = 1 - cdist(x, y, metric='cosine')
    return np.nan_to_num(x, nan=1)
