from rentabot import app
from rentabot.models import Resource

from flask import jsonify
from flask import abort, make_response
from flask import url_for


@app.route('/')
def index():
    return '<h1>Rent-A-Bot</h1>'


def make_public_uri(resource):
    resource = resource.dict
    new_resource = dict()
    for field in resource:
        if field == 'id':
            new_resource['uri'] = url_for('get_resource', bot_id=resource['id'], _external=True)
        else:
            new_resource[field] = resource[field]
    return new_resource


@app.route('/rentabot/api/v1.0/resources', methods=['GET'])
def get_resources():
    return jsonify({'resources': map(make_public_uri, Resource.query.all())})


@app.route('/rentabot/api/v1.0/resources/<int:resource_id>', methods=['GET'])
def get_resource(resource_id):
    resource = Resource.query.filter_by(id=resource_id).first()
    if resource is None:
        abort(404)
    return jsonify({'resource': resource.dict})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)