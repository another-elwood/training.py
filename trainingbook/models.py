__author__ = 'elwood'

import datetime
#from flask import url_for
from trainingbook import db

class Exercise(db.Document):
    name = db.StringField(required=True, max_length=75, unique=True)
    use_weight = db.BooleanField(default=False)
    muscles = db.ListField(db.StringField(max_length=50))
    description = db.StringField(max_length=100)
    meta = {
        'allow_inheritance': True,
        'ordering': ['name']
    }

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Set(db.EmbeddedDocument):
    repetitions = db.IntField(min_value=1, required=True)
    meta = {'allow_inheritance': True}

    def __str__(self):
        return '{0} repetition(s)'.format(self.repetitions)


class WeightedSet(Set):
    weight = db.DecimalField(precision=1, min_value=0, required=True)

    def __str__(self):
        return '{0} repetition(s) with {1} kg'.format(self.repetitions, self.weight)


class PerformedExercise(db.EmbeddedDocument):
    exercise = db.ReferenceField(Exercise)
    sets = db.ListField(db.EmbeddedDocumentField(Set))


class PlannedExercise(db.EmbeddedDocument):
    position = db.IntField(min_value=1, unique=True)
    exercise = db.ReferenceField(Exercise)
    sets = db.ListField(db.EmbeddedDocumentField(Set))
    meta = {
        'indexes': [{ 'fields': ['position'], 'unique': True, 'sparse': True },],
        'ordering': ['position']
    }

    def __str__(self):
        return '#{0} {1}'.format(self.position, self.exercise)


class Cycle(db.Document):
    name = db.StringField(required=True, max_length=50)
    exercises = db.ListField(db.EmbeddedDocumentField(PlannedExercise))

    def __unicode__(self):
        return self.name

    def __str__(self):
        return '{0} with {1} exercise(s)'.format(self.name, len(list(self.exercises)))


class Workout(db.Document):
    cycle = db.ReferenceField(Cycle)
    timestamp = db.DateTimeField(default=datetime.datetime.now, required=True)
    duration = db.IntField(min_value=0)
    motivation = db.IntField(min_value=0, max_value=5)
    exercises = db.ListField(db.EmbeddedDocumentField(PerformedExercise))

    def __str__(self):
        return '"{0}" @ {1} performed {2} exercise(s) with motivation of {3}'.format(self.cycle.name,
                                                                                 self.timestamp,
                                                                                 len(list(self.exercises)),
                                                                                 self.motivation)