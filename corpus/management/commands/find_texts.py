#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Add year data to ElasticSearch index.
"""
import sys
import codecs
import re

from django.core.management.base import BaseCommand
from corpus.models import Titel, Genre


def get_title(text_id):
    try:
        t = Titel.objects.get(pk=text_id)
    except:
        t = None
    return t


def get_year(title):
    m = re.search(r'\d{4}', title.jaar)
    if m:
        return int(m.group(0))
    return None


class Command(BaseCommand):
    help = 'Add year data for plays in the corpus to the ElasticSearch index.'

    def handle(self, *args, **options):
        if len(args) == 1:
            in_file = args[0]
        else:
            print 'Usage: python manage.py find_texts <input>'
            print 'Please provide the name of the input file.'
            sys.exit(1)

        with codecs.open(in_file, 'rb', 'utf-8') as f:
            lines = f.readlines()

        genre_drama = Genre.objects.get(pk=3)
        title_ids = {}

        for line in lines:
            text_id = line[0:13]
            t = get_title(text_id)

            if t:
                if genre_drama in t.genres.all():
                    year = get_year(t)
                    if year <= 1830 and year >= 1600:
                        title_ids[text_id] = None

        for line in lines:
            text_id = line[0:13]
            t = get_title(text_id)

            if t:
                if genre_drama in t.genres.all():
                    if len(t.contains.all()) == 1:
                        t2 = t.contains.all()[0]
                        year = get_year(t2)

                        if year and year <= 1830 and year >= 1600:
                            if t2.ti_id not in title_ids.keys():
                                title_ids[text_id] = None
                                print 'Found older version of', t
                                print t2
                                print ''
                    elif len(t.contains.all()) > 1:
                        print t
                        for t2 in t.contains.all():
                            print '\t', t2

        print '# titles found: {}'.format(len(title_ids.keys()))
        #print '\n'.join(title_ids.keys())
