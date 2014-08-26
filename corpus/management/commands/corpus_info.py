#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Print corpus info to the screen.
"""
from django.core.management.base import BaseCommand
from django.conf import settings

from corpus.models import Titel
from corpus.views import _corpus_ids

class Command(BaseCommand):
    help = 'Print tab separated information about the corpus to the screen.'

    def handle(self, *args, **options):
        print "ID\tJaar\tTitel\tAuteur(s)"

        corpus = Titel.objects.filter(ti_id__in=_corpus_ids) \
                      .order_by('titel').order_by('jaar')

        for t in corpus:
            auteurs = [unicode(a) for a in t.auteurs.all()]

            print "{}\t{}\t{}\t{}".format(t.ti_id,
                                          t.jaar,
                                          t.titel.encode('ascii', 'replace'),
                                          ' & '.join(auteurs) \
                                               .encode('ascii', 'replace'))
