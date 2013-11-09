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

@mod.route('/edit/<id>')
def edit(id):
    exercise = Exercise.objects.get_or_404(id=id)
    form_cls = model_form(exercise.__class__)
    form = form_cls(obj=exercise)
    context = {
            "exercise": exercise,
            "form": form
        }
    return render_template('exercises/edit.html', **context)
    #abort(404)
