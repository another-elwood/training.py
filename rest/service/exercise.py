__author__ = 'elwood'

from flask import Blueprint, request, redirect, render_template, url_for, abort, jsonify, make_response
from rest.models import Exercise

mod = Blueprint('exercises', __name__, url_prefix='/gym/api/v1.0')

@mod.route('/exercises', methods = ['GET'])
def get_exercises():
    exercises = Exercise.objects.all()
    return  jsonify(exercises=[ex.to_dict() for ex in exercises])

@mod.route('/exercises/<id>', methods = ['GET'])
def get_exercise(id):
    exercise = Exercise.objects.get_or_404(id=id)
    return  jsonify(exercise=exercise.to_dict())

@mod.route('/exercises', methods = ['POST'])
def create_exercise():
    if not request.json or not 'name' in request.json:
        abort(400)

    exercise = Exercise()
    exercise.name = request.json['name']
    exercise.use_weight = request.json.get('use_weight', False)
    exercise.muscles = request.json.get('muscles', [])
    exercise.description = request.json.get('description', '')

    # store exercise in database
    # exercise.save()

    return jsonify(exercise=exercise.to_dict()), 201

@mod.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)