from django.db import models

class Entity(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class EntityValue(models.Model):
    name = models.CharField(max_length=140)

    def __unicode__(self):
        return self.name

class EntityScore(models.Model):
    speakingturn = models.ForeignKey('SpeakingTurn')
    entity = models.ForeignKey(Entity)
    entityvalues = models.ManyToManyField(EntityValue)
    score = models.IntegerField()

    def __unicode__(self):
        return '{}: {} - {}'.format(self.speakingturn,
                                    self.entity.name,
                                    self.score)

class Character(models.Model):
    name = models.CharField(max_length=50)
    play = models.ForeignKey('corpus.Titel')
    num_speaking_turns = models.IntegerField()

    def __unicode__(self):
        return '{} ({})'.format(self.name, self.play.titel)

class SpeakingTurn(models.Model):
    character = models.ForeignKey(Character)
    order = models.IntegerField()
    entity = models.ManyToManyField(Entity, through=EntityScore)

    def __unicode__(self):
        return '({}) {}'.format(self.order,
                                      self.character)
