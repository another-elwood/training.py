__author__ = 'elwood'

from flask import Blueprint, render_template

mod = Blueprint('client', __name__, template_folder='client_templates')

@mod.route('/home')
def home():
     return render_template('home.html')

@mod.route('/exercises')
def exercises():
     return render_template('exercises.html')

@mod.route('/cycles')
def cycles():
     return render_template('cycles.html')

@mod.route('/workouts/')
def workouts():
     return render_template('workouts.html')
