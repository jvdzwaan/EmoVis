# -*- coding: utf-8 -*-
"""EntityScore helper functions."""

import numpy as np


def get_r_score(entity1, entity2):
    """Return the r score for two entities.
    r = (e1-e2)/(e1+e2)
    """
    score1 = 0
    score2 = 0
    if entity1:
        score1 = entity1.score
    if entity2:
        score2 = entity2.score

    if not (score1 == 0 and score2 == 0):
        return (score1-score2)/(score1+score2+0.0)
    return 0.0


def moving_average(a, n=3):
    """Calculate the moving average of array a and window size n."""
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n
