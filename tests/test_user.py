from app.models import User
from .base import BaseTest


class TestUser(BaseTest):
    def test_index(self):
        url = '/api/v1/'
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)

    def test_user_registration(self):
        url = '/api/v1/auth/register'
        data = dict(username='kayeli', password='password')
        r = self.client.post(url, data=data)
        self.assertEqual(r.status_code, 201)


    # def test_user_registration(self):
    #     user_credentials = dict(username='kayeli', password='password')
    #     base_url = '/api/v1/'
    #     response = self.client.post('/api/v1/auth/register/',
    #                 data=user_credentials, content_type='application/json', follow_redirects=True)
    #
    #     print (response)
    #     self.assertEqual(response.status_code, 201)
