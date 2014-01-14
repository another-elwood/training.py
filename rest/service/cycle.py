__author__ = 'elwood'

from flask import Blueprint, request, redirect, render_template, url_for, abort

mod = Blueprint('cycles', __name__, url_prefix='/gym/api/v1.0')

@mod.route('/cycles', methods = ['GET'])
def index():
    return "Hello, Cycles!"