__author__ = 'elwood'

import datetime
#from flask import url_for
from rest import db

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

    def to_dict(self):
        values = [
            ('name', self.name),
            ('use_weight', self.use_weight),
            ('muscles', self.muscles),
            ('description', self.description),
        ]
        return dict(values)


class Set(db.EmbeddedDocument):
    repetitions = db.IntField(min_value=1, required=True)
    meta = {'allow_inheritance': True}

    def __str__(self):
        return '{0} repetition(s)'.format(self.repetitions)

    def to_dict(self):
        values = [
            ('repetitions', self.repetitions),
        ]
        return dict(values)


class WeightedSet(Set,):
    weight = db.DecimalField(precision=1, min_value=0, required=True)

    def __str__(self):
        return '{0} repetition(s) with {1} kg'.format(self.repetitions, self.weight)

    def to_dict(self):
        values = [
            ('repetitions', self.repetitions),
            ('weight', float(self.weight)),
        ]
        return dict(values)


class PerformedExercise(db.EmbeddedDocument):
    exercise = db.ReferenceField(Exercise)
    sets = db.ListField(db.EmbeddedDocumentField(Set))

    def to_dict(self):
        values = [
            ('sets', [s.to_dict() for s in self.sets]),
            ('exercise', self.exercise.to_dict()),
        ]
        return dict(values)


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

    def to_dict(self):
        values = [
            ('position', self.position),
            ('sets', [s.to_dict() for s in self.sets]),
            ('exercise', self.exercise.to_dict()),
        ]
        return dict(values)


class Cycle(db.Document):
    name = db.StringField(required=True, max_length=50)
    exercises = db.ListField(db.EmbeddedDocumentField(PlannedExercise))

    def __unicode__(self):
        return self.name

    def __str__(self):
        return '{0} with {1} exercise(s)'.format(self.name, len(list(self.exercises)))

    def to_dict(self):
        values = [
            ('name', self.name),
            ('exercises', [pe.to_dict() for pe in self.exercises]),
        ]
        return dict(values)


class Workout(db.Document):
    cycle = db.ReferenceField(Cycle)
    timestamp = db.DateTimeField(default=datetime.datetime.now, required=True)
    duration = db.IntField(min_value=0)
    motivation = db.IntField(min_value=0, max_value=5)
    exercises = db.ListField(db.EmbeddedDocumentField(PerformedExercise))

    meta = {
            'ordering': ['-timestamp']
    }

    def __str__(self):
        return '"{0}" @ {1} performed {2} exercise(s) with motivation of {3}'.format(self.cycle.name,
                                                                                 self.timestamp,
                                                                                 len(list(self.exercises)),
                                                                                 self.motivation)

    def to_dict(self):
        values = [
            ('timestamp', self.timestamp),
            ('duration', self.duration),
            ('motivation', self.motivation),
            ('exercises', [e.to_dict() for e in self.exercises]),
            ('cycle', self.cycle.to_dict()),
        ]
        return dict(values)