from flask import Blueprint

blueprint = Blueprint('internal', __name__)

@blueprint.route('/ping')
def ping():
    return "pong"
