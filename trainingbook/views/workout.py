__author__ = 'elwood'

from flask import Blueprint, request, redirect, render_template, url_for, abort
from flask.ext.mongoengine.wtf import model_form
from trainingbook.models import Exercise, Cycle, Set, WeightedSet, PlannedExercise, Workout, PerformedExercise
import operator

mod = Blueprint('workouts', __name__, url_prefix='/workouts', template_folder='templates')

@mod.route('/')
def index():
    workouts = Workout.objects.all()
    return render_template('workouts/list.html', workouts=workouts)

@mod.route('/add', methods=['GET', 'POST'])
def add():
    cycles = Cycle.objects.all()
    return render_template('workouts/start.html', cycles=cycles)

@mod.route('/fill/<cycle_id>', methods=['GET', 'POST'])
@mod.route('/fill/<cycle_id>/<id>', methods=['GET', 'POST'])
@mod.route('/fill/<cycle_id>/<id>/<int:position>', methods=['GET', 'POST'])
def fill(cycle_id, id=None, position=0):
    cycle = Cycle.objects.get_or_404(id=cycle_id)
    if id:
        workout = Workout.objects.get_or_404(id=id)
    else:
        workout = Workout(cycle=cycle)
        for planned_exercise in cycle.exercises:
            new_exercise = PerformedExercise(exercise=planned_exercise.exercise, sets=[])
            workout.exercises.append(new_exercise)
        workout.save()
        return redirect(url_for('workouts.fill', cycle_id=cycle.id, id=workout.id))

    # render n-th exercise input
    return render_template('workouts/input.html', workout=workout, position=position)

@mod.route('/view/<id>', methods=['GET'])
def view(id):
    abort(404)

@mod.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id=None):
    abort(404)
