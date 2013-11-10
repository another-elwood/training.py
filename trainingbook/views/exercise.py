__author__ = 'elwood'

from flask import Blueprint, request, redirect, render_template, url_for, abort
from flask.ext.mongoengine.wtf import model_form
from trainingbook.models import Exercise

mod = Blueprint('exercises', __name__, url_prefix='/exercises', template_folder='templates')

@mod.route('/')
def index():
     exercises = Exercise.objects.all()
     return render_template('exercises/list.html', exercises=exercises)

@mod.route('/add')
def add():
    abort(404)

@mod.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    context = get_context(id)

    if request.method == 'POST':
        form = context.get('form')
        if form.validate():
            exercise = context.get('exercise')
            form.populate_obj(exercise)
            exercise.save()
            return redirect(url_for('exercises.index'))
    return render_template('exercises/edit.html', **context)

def get_context(id=None):
    if id:
        # edit
        exercise = Exercise.objects.get_or_404(id=id)
        form_cls = model_form(exercise.__class__)

        if request.method == 'POST':
            form = form_cls(request.form, inital=exercise._data)
            # process single line list
            for muscle in request.form['muscles'].split('\r\n'):
                form.muscles.append_entry(muscle)
        else:
            form = form_cls(obj=exercise)
    else:
        # create
        exercise = Exercise()
        form_cls = model_form(exercise.__class__)
        form = form_cls(request.form)

    context = {
            "exercise": exercise,
            "form": form,
            "create": id is None
        }
    return context