__author__ = 'elwood'

from flask import Blueprint, request, redirect, render_template, url_for, abort, jsonify
from rest.models import Workout

mod = Blueprint('workouts', __name__, url_prefix='/gym/api/v1.0')

@mod.route('/workouts', methods = ['GET'])
def get_workouts():
    workouts = Workout.objects.all()
    return  jsonify(result=[w.to_dict() for w in workouts])