# -*- coding: utf-8 -*-
"""EntityScore helper functions."""


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
