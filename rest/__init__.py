__author__ = 'elwood'

from flask import Flask, abort
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {"DB": "trainingbook"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"
app.config['WTF_CSRF_ENABLED'] = False

db = MongoEngine(app)

## register blueprints
#from trainingbook.views import exercise, cycle, workout
#app.register_blueprint(exercise.mod)
#app.register_blueprint(cycle.mod)
#app.register_blueprint(workout.mod)

@app.errorhandler(500)
def custom_error(e):
    abort(500)

if __name__ == '__main__':
    app.run()
