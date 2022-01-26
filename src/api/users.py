from urllib import response
from attr import validate
from flask import Blueprint, request
from flask_restx import Resource, Api, fields

from src import db
from src.api.models import User

users_blueprint = Blueprint('users', __name__)
api = Api(users_blueprint)

# validate the payload against this api model
user = api.model('User', {
    'id': fields.Integer(readOnly=True),
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'created_date': fields.DateTime,
})

class UserList(Resource):

    @api.expect(user, validate=True)
    def post(self):
        post_data  = request.get_json()
        username = post_data.get('username')
        email = post_data.get('email')

        response_object = {}

        # make sure the user does not already exist
        user = User.query.filter_by(email=email).first()
        if user:
            response_object['message'] = 'Sorry. That email already exists.'
            return response_object, 400

        db.session.add(
            User(username=username, email=email)
        )
        db.session.commit()

        response_object['message'] = f'{email} was added!'
        return response_object, 201

class Users(Resource):

    # serialize the response as a JSON object defined in the user API model
    @api.marshal_with(user)
    def get(self, id):
        user =  User.query.filter_by(id=id).first()

        if not user:
            api.abort(404, f"User {id} does not exist")
        return user, 200

api.add_resource(UserList, '/users')
api.add_resource(Users, '/users/<int:id>')

