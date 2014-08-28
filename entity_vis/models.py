from django.db import models

from corpus.models import Titel

class Entity(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class Character(models.Model):
    name = models.CharField(max_length=50)
    play = models.ForeignKey(Titel)
    num_speaking_turns = models.IntegerField()

    def __unicode__(self):
        return '{} ({})'.format(self.name, self.play.titel)

class SpeakingTurn(models.Model):
    character = models.ForeignKey(Character)
    order = models.IntegerField()
    entity = models.ManyToManyRel(Entity)
    score = models.IntegerField()

    def __unicode__(self):
        return '({}) {}'.format(self.order,
                                      self.character)
