from flask import current_app
from app import db
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                         as Serializer, BadSignature, SignatureExpired)
from config import config

class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return "<User %s>" %self.username

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration = 600):
        """
        the token is an encrypted version of a dictionary that has the id of the user.
        The token will also have an expiration time embedded in it, 
        which by default will be of ten minutes
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return 'valid token, but expired!'
        except BadSignature:
            return 'invalid token'
        user = User.query.get(data['id'])
        return user
