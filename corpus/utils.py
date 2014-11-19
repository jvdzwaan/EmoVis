#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Utility functions for corpus.
"""

import re


def get_year(year_string):
    """Extract the publication year of a title from a string.
    """
    m = re.search(r'\d{4}', year_string)
    if m:
        return int(m.group(0))
    m = re.search(r'17de', year_string)
    if m:
        return int(1600)
    return None
