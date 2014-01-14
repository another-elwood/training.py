__author__ = 'elwood'

from flask import Blueprint, request, redirect, render_template, url_for, abort

mod = Blueprint('workouts', __name__, url_prefix='/gym/api/v1.0')

@mod.route('/workouts', methods = ['GET'])
def index():
    return "Hello, Workouts!"