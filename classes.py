__author__ = 'elwood'

from mongoengine import *

class Exercise(Document):
    name = StringField(required=True, max_length=75)
    muscles = ListField(StringField(max_length=50))
    meta = {'allow_inheritance': True}

class Set(EmbeddedDocument):
    repetitions = IntField(min_value=1, required=True)
    meta = {'allow_inheritance': True}

class WeightedSet(Set):
    weight = DecimalField(precision=1, min_value=0)

class PerformedExercise(EmbeddedDocument):
    exercise = ReferenceField(Exercise)
    sets = ListField(EmbeddedDocumentField(Set))

class Cycle(Document):
    name = StringField(required=True, max_length=50)
    exercises = ListField(ReferenceField(Exercise))
    def __str__(self):
        return '{0} with {1} exercise(s)'.format(self.name, len(list(self.exercises)))

class Workout(Document):
    cycle = ReferenceField(Cycle)
    timestamp = DateTimeField(required=True)
    motivation = IntField(min_value=0, max_value=5)
    exercises = ListField(EmbeddedDocumentField(PerformedExercise))
    def __str__(self):
        return '"{0}" @ {1} performed {2} exercise(s) with motivation of {3}'.format(self.cycle.name,
                                                                                 self.timestamp,
                                                                                 len(list(self.exercises)),
                                                                                 self.motivation)