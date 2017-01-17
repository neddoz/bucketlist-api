from flask_testing import TestCase
from app import create_app, db, api
from app.models import User, BucketList
from app.endpoints.user import Index, RegisterUser, LoginUser
from app.endpoints.bucketlist import BucketListRepo

class BaseTest(TestCase):

    def create_app(self):
        # pass in test configuration
        app = create_app('testing')
        return app

    def setUp(self):
        self.client = self.create_app().test_client()
        self.api = api
        db.create_all()
        api.add_resource(Index, '/', '/api/v1', endpoint='index')
        api.add_resource(RegisterUser, '/auth/register', endpoint='register')
        # api.add_resource(LoginUser, 'api/v1/auth/login', endpoint='login')
        # api.add_resource(BucketListRepo, 'api/v1/bucketlists/', endpoint='bucketlist')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
