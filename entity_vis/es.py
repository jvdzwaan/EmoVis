# -*- coding: utf-8 -*-
"""ElasticSearch functionality."""

from elasticsearch import Elasticsearch


def _es():
    # TODO: make es instance configurable (via settings.py)
    return Elasticsearch()


def search_query(query, doc_type):
    return _es().search('embodied_emotions', doc_type=doc_type, body=query)
