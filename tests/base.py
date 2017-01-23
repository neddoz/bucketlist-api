from flask import json
from flask_testing import TestCase
from app import create_app, db, api
from app.models import User, BucketList
from app.endpoints.user import Index, RegisterUser, LoginUser
from app.endpoints.bucketlist import BucketListRepo
from app.endpoints.bucketlist_items import BucketListItemsRepo

class BaseTest(TestCase):

    def create_app(self):
        # pass in test configuration
        app = create_app('testing')
        return app

    def setUp(self):
        self.client = self.create_app().test_client()
        self.user_credentials = dict(username='kayeli', password='password')
        db.create_all()
        api.add_resource(Index, '/', '/api/v1', endpoint='index')
        api.add_resource(RegisterUser, '/auth/register', endpoint='register')
        api.add_resource(LoginUser, '/auth/login', endpoint='login')
        api.add_resource(BucketListItemsRepo, '/bucketlists/<id>/items/',
                                endpoint='bucketlist_items')
        api.add_resource(BucketListItemsRepo, '/bucketlists/<id>/items/<item_id>')
        api.add_resource(BucketListRepo, '/bucketlists/<id>',
                                endpoint='bucketlists')
        api.add_resource(BucketListRepo, '/bucketlists/')
        # api.add_resource(BucketListRepo, 'api/v1/bucketlists/', endpoint='bucketlist')

        #register a user
        self.client.post('/api/v1/auth/register', data=self.user_credentials)

        self.response = self.client.post('/api/v1/auth/login', data=self.user_credentials)
        self.response_data_in_json_format = json.loads(self.response.data.decode('utf-8'))

        self.token = 'Token '+self.response_data_in_json_format['token']
        self.headers = {'Authorization': self.token}
    def tearDown(self):
        db.session.remove()
        db.drop_all()
