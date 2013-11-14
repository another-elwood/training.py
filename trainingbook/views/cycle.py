__author__ = 'elwood'

from flask import Blueprint, request, redirect, render_template, url_for, abort
from flask.ext.mongoengine.wtf import model_form
from trainingbook.models import Exercise, Cycle

mod = Blueprint('cycles', __name__, url_prefix='/cycles', template_folder='templates')

@mod.route('/')
def index():
    cycles = Cycle.objects.all()
    return render_template('cycles/list.html', cycles=cycles)

@mod.route('/add', methods=['GET', 'POST'])
def add():
    abort(404)

@mod.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    abort(404)

@mod.route('/delete/<id>')
def delete(id):
    abort(404)