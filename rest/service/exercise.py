__author__ = 'elwood'

from flask import Blueprint, request, redirect, render_template, url_for, abort, jsonify
from rest.models import Exercise

mod = Blueprint('exercises', __name__, url_prefix='/gym/api/v1.0')

@mod.route('/exercises', methods = ['GET'])
def get_exercises():
    exercises = Exercise.objects.all()
    return  jsonify(result=[ex.to_dict() for ex in exercises])


