from flask import current_app
from app import db
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                         as Serializer, BadSignature, SignatureExpired)
from config import config
from datetime import datetime


class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    bucketlist = db.relationship('BucketList', backref='users',
                                cascade='all, delete', lazy='dynamic')

    def __repr__(self):
        return "<User %s>" %self.username

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration = 3600):
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
            user_id = data['id']
            return user_id
        except SignatureExpired:
            return 'valid token, but expired!'
        except BadSignature:
            return 'invalid token'


class BucketList(db.Model):

    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=datetime.now)
    created_by = db.Column(db.String(20), nullable=False)
    date_modified = db.Column(db.DateTime, onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship('BucketlistItems', backref='bucketlists',
                                cascade='all, delete', lazy='dynamic')

    def __repr__(self):
        return "<BucketList %s>" %self.name


class BucketlistItems(db.Model):

    __tablename__ = 'bucketlistitems'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime, onupdate=datetime.now)
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def __repr__(self):
        return "<BucketlistItems %s>" %self.name
