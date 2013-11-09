__author__ = 'elwood'

import datetime
#from flask import url_for
from trainingbook import db

class Exercise(db.Document):
    name = db.StringField(required=True, max_length=75)
    muscles = db.ListField(db.StringField(max_length=50))
    meta = {
        'allow_inheritance': True,
        'ordering': ['name']
    }

    def __unicode__(self):
        return self.name


class Set(db.EmbeddedDocument):
    repetitions = db.IntField(min_value=1, required=True)
    meta = {'allow_inheritance': True}


class WeightedSet(Set):
    weight = db.DecimalField(precision=1, min_value=0, required=True)


class PerformedExercise(db.EmbeddedDocument):
    exercise = db.ReferenceField(Exercise)
    sets = db.ListField(db.EmbeddedDocumentField(Set))


class Cycle(db.Document):
    name = db.StringField(required=True, max_length=50)
    exercises = db.ListField(db.ReferenceField(Exercise))

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