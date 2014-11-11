# -*- coding: utf-8 -*-
"""ElasticSearch functionality."""

from elasticsearch import Elasticsearch


def _es():
    # TODO: make es instance configurable (via settings.py)
    return Elasticsearch()


def search_query(query, doc_type):
    return _es().search('embodied_emotions', doc_type=doc_type, body=query)


def match_all():
    """Return match_all query.
    """
    return {
        "query": {
            "match_all": {}
        },
        "size": 0
    }


def term_query(field, value, size=0):
    q = {
        "query": {
            "term": {
                field: {
                    "value": value
                }
            }
        }
    }
    if size:
        q["size"] = size

    return q


def doc_count(query, doc_type):
    result = _es().count('embodied_emotions', doc_type=doc_type, body=query)
    return result.get('count', 0)
