__author__ = 'elwood'

from flask import Blueprint, request, redirect, render_template, url_for
from flask.ext.mongoengine.wtf import model_form
from trainingbook.models import Exercise

mod = Blueprint('exercises', __name__, url_prefix='/exercises', template_folder='templates')

@mod.route('/')
def index():
     exercises = Exercise.objects.all()
     return render_template('exercises/list.html', exercises=exercises)
