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
    return get_page()

@mod.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    return get_page(id)

@mod.route('/delete/<id>')
def delete(id):
    abort(404)

def get_page(id=None):
    context = get_context(id)

    if request.method == 'POST':
        form = context.get('form')
        if form.validate():
            cycle = context.get('cycle')
            form.populate_obj(cycle)
            cycle.save()
            return redirect(url_for('cycles.index'))
    return render_template('cycles/edit.html', **context)

def get_context(id=None):
    if id:
        # edit
        cycle = Cycle.objects.get_or_404(id=id)
        form_cls = model_form(cycle.__class__)

        if request.method == 'POST':
            form = form_cls(request.form, inital=cycle._data)
        else:
            form = form_cls(obj=cycle)
    else:
        # create
        cycle = Cycle()
        form_cls = model_form(cycle.__class__)
        form = form_cls(request.form)

    context = {
            "cycle": cycle,
            "form": form,
            "create": id is None
        }
    return context
