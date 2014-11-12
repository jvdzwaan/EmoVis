"""Utility functions for the Embodied Emotions Visualizations app.
"""
import json


def get_from_body(request, key):
    """Get the value(s) for key from the request body."""
    # angular sends post data in the request.body
    if request.body:
        body = json.loads(request.body)
        return body.get(key)
    return None
