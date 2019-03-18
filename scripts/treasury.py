#!flask/bin/python
# -*- coding: utf8

from flask import (
    Flask,
    jsonify,
    abort,
    make_response
)
from flask_restful import (
    Api,
    Resource,
    reqparse,
    fields,
    marshal
)

app = Flask(__name__, static_url_path="")
api = Api(app)

cheer_fields = {
    'memo': fields.String,
    'year': fields.Integer,
    'month': fields.Integer,
    'donation_range': fields.String,
    'uri': fields.Url('cheer')
}

cheers = [
    {
        'id': 1,
        'memo': u'I ♥  Inkscape',
        'year': 2019,
        'month': 3,
        'donation_range': "$5-10"
    },
    {
        'id': 1,
        'memo': u'Please keep up the great work!\nI use Inkscape every day.',
        'year': 2019,
        'month': 3,
        'donation_range': "$5-10"
    }
]

class CheerListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('memo', type=str, default="", location='json')
        self.reqparse.add_argument('value', type=float, location='json')
        super(CheerListAPI, self).__init__()

    def get(self, id):
        return {'cheers': marshal(cheer, cheer_fields) for cheer in cheers}, 201

api.add_resource(CheerListAPI, '/treasury/api/v1.0/cheers', endpoint='cheers')


if __name__ == '__main__':
    app.run(debug=True)
