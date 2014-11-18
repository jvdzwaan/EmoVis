#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Add year data to ElasticSearch index.
"""
from elasticsearch import Elasticsearch, helpers

from django.core.management.base import BaseCommand
from corpus.models import Titel

from django.conf import settings


class Command(BaseCommand):
    help = 'Add year data for plays in the corpus to the ElasticSearch index.'

    def handle(self, *args, **options):
        index_name = settings.ES_INDEX
        doc_type = 'event'

        # Get text ids
        es = Elasticsearch()
        query = {
            'query': {'match_all': {}},
            'size': 0,
            'aggregations': {
                'ids': {
                    'terms': {
                        'field': 'text_id',
                        'size': 1000
                    }
                }
            }
        }

        result = es.search(index=index_name, doc_type=doc_type, body=query)
        text_ids = [b.get('key') for b in result.get('aggregations')
                                                .get('ids').get('buckets')]
        for text_id in text_ids:
            title = Titel.objects.get(pk=text_id)
            print '({}) {}'.format((text_ids.index(text_id)+1), title)

            subtitles = title.contains.all()

            year = None
            if not subtitles:
                # the year we want to save to ES is the year of title
                year = title.jaar
            elif len(subtitles) == 1:
                # the year we want to save to ES is the year of the subtitle
                year = subtitles[0].jaar
            else:
                print '\tMultiple subtitles - unclear which one to choose'
                for t in subtitles:
                    print '\t', t
                print 'Will not be saved to ElasticSearch.'

            if year:
                print year

                # get all events for text id
                q = {
                    "query": {
                        "term": {
                            "text_id": {
                                "value": text_id
                            }
                        }
                    }
                }

                results = helpers.scan(client=es, query=q)
                for r in results:
                    # save year to ES
                    doc = {
                        'doc': {
                            'year': int(year)
                        }
                    }
                    es.update(index=index_name, doc_type=doc_type,
                              id=r.get('_id'), body=doc)
                print ''
