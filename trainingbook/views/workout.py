__author__ = 'elwood'

from flask import Blueprint, request, redirect, render_template, url_for, abort
from flask.ext.mongoengine.wtf import model_form
from trainingbook.models import Exercise, Cycle, Set, WeightedSet, PlannedExercise, Workout
import operator

mod = Blueprint('workouts', __name__, url_prefix='/workouts', template_folder='templates')

@mod.route('/')
def index():
    workouts = Workout.objects.all()
    return render_template('workouts/list.html', workouts=workouts)