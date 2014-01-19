__author__ = 'elwood'

from flask import Blueprint, request, redirect, render_template, url_for, abort, jsonify, make_response
from rest.models import Exercise

mod = Blueprint('exercises', __name__, url_prefix='/gym/api/v1.0')

@mod.route('/exercises', methods = ['GET'])
def get_exercises():
    exercises = Exercise.objects.all()
    return jsonify(exercises=[ex.to_dict() for ex in exercises])

@mod.route('/exercises/<id>', methods = ['GET'])
def get_exercise(id):
    exercise = Exercise.objects.get_or_404(id=id)
    return jsonify(exercise=exercise.to_dict())

@mod.route('/exercises', methods = ['POST'])
def create_exercise():
    if not request.json or not 'name' in request.json:
        abort(400)

    exercise = parse_json_data(request.json)
    exercise.save()

    return jsonify(exercise=exercise.to_dict()), 201

@mod.route('/exercises/<id>', methods = ['PUT'])
def update_exercise(id):
    exercise = Exercise.objects.get_or_404(id=id)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) is not str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'use_weight' in request.json and type(request.json['use_weight']) is not bool:
        abort(400)

    exercise = parse_json_data(request.json, exercise)
    exercise.save()
    return jsonify(exercise=exercise.to_dict())

@mod.route('/exercises/<id>', methods = ['DELETE'])
def delete_exercise(id):
    exercise = Exercise.objects.get_or_404(id=id)
    exercise.delete()
    return jsonify(result=True)

@mod.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

def parse_json_data(json, exercise=None):
    if not exercise:
        exercise = Exercise(use_weight=False)
    exercise.name = json['name']

    if 'use_weight' in request.json:
        exercise.use_weight = json['use_weight']

    if not exercise.muscles or 'muscles' in request.json:
        exercise.muscles = json.get('muscles', [])

    if not exercise.description or 'description' in request.json:
        exercise.description = json.get('description', '')

    return exercise