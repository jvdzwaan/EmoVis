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


def relevant(title, genre_drama):
    if genre_drama in title.genres.all():
        year = get_year(title)
        if year <= 1830 and year >= 1600:
            return True
    return False


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
                # add title if it has genre drama and is from the right time
                # period
                if relevant(t, genre_drama):
                    title_ids[text_id] = None

                # add title if it contains at least one title that has genre
                # drama and is from the right time period
                contained_titles = t.contains.all()
                add = False
                for t2 in contained_titles:
                    if relevant(t2, genre_drama):
                        add = True
                if add:
                    title_ids[text_id] = None

        print '# titles found: {}'.format(len(title_ids.keys()))
        #print '\n'.join(title_ids.keys())
