from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from .models import User

#for username and password authentication
basic_authorization = HTTPBasicAuth()

#for token authentication
token_based_authentication = HTTPTokenAuth('Token')

#To grant access to the endpoint, one of the authentication methods must validate.
multiple_auth = MultiAuth(basic_authorization, token_based_authentication)

@basic_authorization.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True

@token_based_authentication.verify_token
def verify_token(token):
    user_id = User.verify_auth_token(token)
    if user_id:
        g.user = User.query.filter_by(id=user_id).first()
        return True
    return False

@basic_authorization.error_handler
@token_based_authentication.error_handler
def auth_error():
    return {"message":"Sorry Access Denied!"}, 401
