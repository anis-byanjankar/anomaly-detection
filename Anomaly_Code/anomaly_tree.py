import math
import numpy as np
from read_file import *
from compute_features import *
from extract_pixel import *
import random

# training forest
class iForest:
    '''Input: X - features data frame for individual tile
              t - number or trees to fit
              n - subsampling size
       Output: a set of t of iTrees
       '''
    def __init__(self, X, t=40, n=256):
         self.x = X
         self.t = t
         self.n = n
         self.forest = []

    def populate(self):
        for i in range(self.t):
            samples = self.x[np.random.randint(self.x.shape[0], size = self.n),:]
            self.forest.append(iTree(samples))
        return self.forest

class exNode:
    def __init__(self, size):
        self.size = size
        self.isLeaf = True

class inNode:
    def __init__(self, Left, Right, SplitAtt, SplitValue, size):
        self.Left = Left
        self.Right = Right
        self.SplitAtt = SplitAtt
        self.SplitValue = SplitValue
        self.size = size
        self.isLeaf = False

def iTree(X):
    '''Input: X: subsampled dataset
       Output: isolation forest tree
    '''
    n = len(X)
    if n <= 1:
        return exNode(n)
    else:
        q = random.randint(0,5)
        subset_column = X[:,q]
        minimum = np.amin(subset_column)
        maximum = np.amax(subset_column)
        if minimum == maximum:
            return exNode(n)
        p1 = random.uniform(minimum, maximum)
        p2 = random.uniform(minimum, maximum)
        p3 = random.uniform(minimum, maximum)
        p = np.median([p1,p2,p3])
        x_l = X[subset_column < p]
        x_r = X[subset_column >= p]
        return inNode(iTree(x_l), iTree(x_r), q, p, n)

# Evaluation
def eval_tree(x, T, h = 20, e = 0):
    '''Input: x - one row from features dataset
              T - iTree
              h - height limit
              e - current path length
       Output - path length of x
    '''
    if T.isLeaf or e >= h:
        return e + path_length(T.size)
    if x[T.SplitAtt] < T.SplitValue:
        return eval_tree(x, T.Left, h, e+1)
    else:
        return eval_tree(x, T.Right, h, e+1)

def path_length(n):
    '''Input: n - sample size
       Output: adjusted score for eval_tree
    '''
    if n > 2:
        return 2 * (math.log(n - 1) + 0.5772156649) - 2 * (n - 1) / n
    if n == 2:
        return 1
    else:
        return 0

def anomaly_frames(frames, t, n, tile):
    '''Input: frames - features data frame for one tile
              t - number of trees to fit
              n - subsample size
              tile: tile coordinates
        Output: evaluation score for a tile'''
    topleft = [tile[1], tile[0]]
    bottomright = [tile[3], tile[2]]
    x = get_features(frames, topleft, bottomright)
    forest = iForest(x, t, n).populate()
    score_collect = []
    for frame in range(x.shape[0]):
        path = []
        for t in forest:
            eval = eval_tree(x[frame], t)
            path.append(eval)
        score = 2 ** (-np.mean(path) / path_length(x.shape[0]))
        score_collect.append(score)
    return score_collect
