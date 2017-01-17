from flask import jsonify
from flask_restful import Resource, reqparse, abort
from app.models import User
from app import db
from app.auth import multiple_auth
from flask import g


class Index(Resource):
    # decorators = [multiple_auth.login_required]
    def get(self):
        return 'welcome!', 200


class RegisterUser(Resource):

    def post(self):
        #getting the username and password from the post request
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='Username for a new user!')
        parser.add_argument('password', type=str, help='Password to create user')
        args = parser.parse_args()
        username = args.username
        password = args.password

        #validation
        if username is None or password is None:
            abort(400, msg='Password and username required!')
        if User.query.filter_by(username=username).first() is not None:
             abort(400, msg='A User with the same name already exists!')

        #create a user instance
        user = User(username=username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return "User Registration success!", 201


class LoginUser(Resource):

    def post(self):
        #getting the username and password from the post request
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='username!')
        parser.add_argument('password', type=str, help='Password')
        args = parser.parse_args()
        username = args.username
        password = args.password

        #validation
        if username is None or password is None:
            abort(400, msg='Password and username required!')

        user = User.query.filter_by(username=username).first()

        #for wrong username provided
        if not user or not user.verify_password(password):
            abort(400, msg='Sorry user not found check credentials!')

        #return a token for use on subsequent requests
        token = user.generate_auth_token()
        return { 'token': token.decode('ascii') }, 200
