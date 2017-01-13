from flask_testing import TestCase
from app import create_app, db

class MyTest(TestCase):

    def create_app(self):
        # pass in test configuration
        return create_app('testing')

    def setUp(self):
        self.client = self.create_app().test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
