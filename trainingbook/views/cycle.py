__author__ = 'elwood'

from flask import Blueprint, request, redirect, render_template, url_for, abort
from flask.ext.mongoengine.wtf import model_form
from trainingbook.models import Exercise, Cycle, Set, WeightedSet, PlannedExercise
import operator

mod = Blueprint('cycles', __name__, url_prefix='/cycles', template_folder='templates')

@mod.route('/')
def index():
    cycles = Cycle.objects.all()
    for cycle in cycles:
        cycle.exercises.sort(key=operator.attrgetter('position'))
    return render_template('cycles/list.html', cycles=cycles)

@mod.route('/add', methods=['GET', 'POST'])
def add():
    return get_page()

@mod.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    return get_page(id)

@mod.route('/delete/<id>')
def delete(id):
    cycle = Cycle.objects.get_or_404(id=id)
    cycle.delete()
    return redirect(url_for('cycles.index'))


@mod.route('/test', methods=['GET'])
def get_page(id=None):
    context = get_context(id)

    if request.method == 'POST':
        cycle = context.get("cycle")
        update_cycle(cycle)
        cycle.save()
        return redirect(url_for('cycles.index'))

    return render_template('cycles/edit.html', **context)

def update_cycle(cycle):
    form = request.form

    # add new exercise(s)
    exercise_counter = len(cycle.exercises) + 1
    form_exercise = "exercise-{0}".format(exercise_counter)
    while form_exercise in form:
        actual_exercise = Exercise.objects.get(id=form[form_exercise])
        new_exercise = PlannedExercise(
            position = exercise_counter,
            exercise = actual_exercise,
            sets = []
        )
        cycle.exercises.append(new_exercise)

        exercise_counter += 1
        form_exercise = "exercise-{0}".format(exercise_counter)

    # update sets
    for i in range(len(cycle.exercises)):
        ex = cycle.exercises[i]
        set_counter = 1
        use_weight = ex.exercise.use_weight

        form_reps = "set-{0}-{1}-reps".format(i+1, set_counter)

        while form_reps in form:
            form_weight = "set-{0}-{1}-weight".format(i+1, set_counter)

            if len(ex.sets) >= set_counter:
                # update set
                ex.sets[set_counter-1].repetitions = form[form_reps]
                if use_weight:
                    ex.sets[set_counter-1].weight = form[form_weight]
            else:
                # add new set
                if use_weight:
                    new_set = WeightedSet(
                        repetitions = form[form_reps],
                        weight = form[form_weight])
                else:
                    new_set = Set(repetitions = form[form_reps])
                ex.sets.append(new_set)

            set_counter += 1
            form_reps = "set-{0}-{1}-reps".format(i+1, set_counter)

    # reorder exercises
    if form["order"]:
        order = [int(x) for x in form["order"][:-1].split(",")]
        cycle.exercises = [cycle.exercises[i-1] for i in order]

        # set new position
        for i in range(len(cycle.exercises)):
            cycle.exercises[i].position = i + 1

def get_context(id=None):
    exercises = Exercise.objects.all()

    if id:
        # edit
        cycle = Cycle.objects.get_or_404(id=id)
        cycle.exercises.sort(key=operator.attrgetter('position'))
    else:
        # create
        cycle = Cycle()

    context = {
            "cycle": cycle,
            "exercises": exercises,
            "create": id is None
        }
    return context
