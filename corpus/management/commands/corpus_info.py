#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Print corpus info to the screen.
"""
from django.core.management.base import BaseCommand

from corpus.models import Titel
from corpus.views import _corpus_ids, _annotation_ids

class Command(BaseCommand):
    help = 'Print tab separated information about the corpus to the screen.'

    def handle(self, *args, **options):
        print "ID\tJaar\tSubgenre(s)\tTitel\tAuteur(s)"

        corpus = Titel.objects.filter(ti_id__in=_annotation_ids) \
                      .order_by('titel')

        for t in corpus:
            auteurs = [unicode(a) for a in t.auteurs.all()]
            subgenres = [unicode(g) for g in t.subgenres.all()]

            #contains = t.contains.all()
            #if len(contains) == 1:
            #    j = contains[0].jaar
            #else:
            #    j = t.jaar

            print "{}\t{}\t{}\t{}\t{}".format(t.ti_id,
                                              t.jaar,
                                              ' & '.join(subgenres),
                                              t.titel.encode('utf-8'),
                                              ' & '.join(auteurs)
                                                   .encode('utf-8'))
