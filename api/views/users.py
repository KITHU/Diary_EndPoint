from flask import request
from flask_restplus import Resource, reqparse
from marshmallow import ValidationError

from main import api, bcrypt
from api.schema.userschema import UserSchema
from api.models.database import db
from api.models.usermodel import UserModel

userschema = UserSchema()


@api.route('/auth/login')
class Login(Resource):
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email',required=True, type=str)
        parser.add_argument('password',required=False, type=str)
        args = parser.parse_args()
        user = UserModel.get_by_email(args.email)
        if user and bcrypt.check_password_hash(user.password, args.password):
            return {'message': 'you are logined in'},200  
        return {'message': 'Wrong email or password'}


@api.route('/auth/signup')
class SignUp(Resource):
    def post(self):
        try:
            user_json = request.get_json()
            user_data = userschema.load(user_json)
        except ValidationError as err:
            return err.messages,400
        if UserModel.get_by_email(user_data.email):
            return {'message': "user already exist"},400
        pw_hash = bcrypt.generate_password_hash(user_data.password).decode('utf-8')
        user_data.password = pw_hash
        user_data.save()
        return {'message': userschema.dump(user_data)}, 201


@api.route('/auth/confirm')
class Confirm(Resource):
    def post(self):
        return {'message': 'confirm user and activate them'}


@api.route('/auth/reset')
class Reset(Resource):
    def post(self):
        return {'message': 'reset user password'}
