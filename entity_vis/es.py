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


def term_query(field, value):
    return {
        "query": {
            "term": {
                field: {
                    "value": value
                }
            }
        },
        "size": 0
    }
