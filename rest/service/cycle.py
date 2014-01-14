__author__ = 'elwood'

from flask import Blueprint, request, redirect, render_template, url_for, abort, jsonify
from rest.models import Cycle

mod = Blueprint('cycles', __name__, url_prefix='/gym/api/v1.0')

@mod.route('/cycles', methods = ['GET'])
def get_cycles():
    cycles = Cycle.objects.all()
    dictlist = [c.to_dict() for c in cycles]
    return  jsonify(result=dictlist)