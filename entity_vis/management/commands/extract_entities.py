#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Extract entities from FoLiA XML files and insert counts into the database.
"""
from bs4 import BeautifulSoup
from collections import Counter

import imp
bs4_helpers = imp.load_source('bs4_helpers',
                              '/home/jvdzwaan/Dropbox/code/embodied_emotions'
                              '_scripts/emotools/bs4_helpers.py')

plays = imp.load_source('plays',
                        '/home/jvdzwaan/Dropbox/code/embodied_emotions'
                        '_scripts/emotools/plays.py')

from django.core.management.base import BaseCommand
from entity_vis.models import Character, Entity, SpeakingTurn, EntityScore
from corpus.models import Titel


class Command(BaseCommand):
    args = '<entity-class, FoLiA XML file>'
    help = 'Extract entity counts from the FoLiA XML file and add them to ' \
           'the database. Entity counts are extracted for each speaker turn.'

    def handle(self, *args, **options):
        entity_class = None
        folia_file = None

        if len(args) > 0:
            entity_class = args[0]
        if len(args) > 1:
            folia_file = args[1]

        self.stdout.write(entity_class)
        self.stdout.write(folia_file)

        if entity_class and folia_file:
            with open(folia_file, 'r') as f:
                soup = BeautifulSoup(f, 'xml')

            # play_id
            play_id = plays.get_play_id(soup)
            self.stdout.write('Play ID: '+play_id)
            play = Titel.objects.get(pk=play_id)

            speakerturns = soup.find_all(bs4_helpers.speaker_turn)

            # character information
            self.stdout.write('Extracting characters...')
            characters = plays.get_characters(speakerturns)
            for name in characters:
                self.stdout.write(' '+name)
                Character.objects.get_or_create(
                    name=name,
                    play=play,
                    num_speaking_turns=characters[name])

            # entity information
            self.stdout.write('\nExtracting entities...')
            entities = plays.get_entities(soup, entity_class)
            for e in entities:
                self.stdout.write(' {}'.format(e))
                Entity.objects.get_or_create(name=e)

            # speaker turn / entity information
            self.stdout.write('\nExtracting speaker turns...')
            for sp in speakerturns:
                name = plays.extract_character_name(sp.get('actor'))
                c = Character.objects.get(name=name, play=play)

                s = SpeakingTurn(character=c,
                                 order=(speakerturns.index(sp)+1))
                s.save()

                self.stdout.write(' {}'.format(unicode(s)))

                # entity scores
                entity_counter = Counter()
                entities = sp.find_all(bs4_helpers.entity)
                for e in entities:
                    if e.get('class').startswith('{}-'.format(entity_class)):
                        entity_counter[e.get('class')] += 1

                for ent in entity_counter:
                    e = Entity.objects.get(name=ent)
                    es = EntityScore(entity=e,
                                     speakingturn=s,
                                     score=entity_counter[ent])
                    es.save()

                    self.stdout.write('  {}'.format(es))
