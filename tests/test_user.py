from app.models import User
from tests import base
from flask import json

BaseTest = base.BaseTest

class TestUser(BaseTest):
    def test_index(self):
        url = '/api/v1/'
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)

    def test_registration(self):
        user_credentials = dict(username='beatrice', password='password')
        url = '/api/v1/auth/register'
        response = self.client.post(url, data=user_credentials)
        self.assertEqual(response.status_code, 201)

        #test for creating a user with the same name
        response = self.client.post(url, data=user_credentials)
        self.assertTrue(response.data,
                        'A User with the same name already exists!')
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        #test a user cannot login with a password or useranem
        user_credentials = dict(username='kayeli')
        response = self.client.post('/api/v1/auth/login', data=user_credentials)
        self.assertTrue(response.data, 'Password and username required!')

        self.client.post('/api/v1/auth/register', data=user_credentials)
        user_credentials = dict(username='kayeli', password='password')
        #register a user
        self.client.post('/api/v1/auth/register', data=user_credentials)

        #try accessing the user with the credentials
        response = self.client.post('/api/v1/auth/login', data=user_credentials)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data.decode('utf-8'))

        #try accesing with the wrong credentials
        wrong_credentials = dict(username='vivian', password='12345')
        response = self.client.post('/api/v1/auth/login', data=wrong_credentials)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.data,
                        'Sorry user not found check credentials!')

    def test_authorization(self):
        # #accessing a route without a token
        # response = self.client.get('/api/v1/bucketlists/')
        # self.assertIn('Sorry Access Denied!', response.data.decode('utf-8'))

        #create a bucketlist
        bucketlist_data = {"name": "Bucket list"}
        response = self.client.post('/api/v1/bucketlists/',
                    data=bucketlist_data,
                    headers=self.headers)
        self.assertEqual(response.status_code, 201)

        user_credentials = dict(username='person', password='password')
        #register a user
        self.client.post('/api/v1/auth/register', data=user_credentials)

        #check  kayeli cannot access the created bucketlist
        response = self.client.post('/api/v1/auth/login', data=user_credentials)
        response_data_in_json_format = json.loads(response.data.decode('utf-8'))

        token = 'Token '+response_data_in_json_format['token']
        headers = {'Authorization': token}

        response = self.client.get('/api/v1/bucketlists/1',
                    headers=headers)
        self.assertIn('Not Found!', response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 404)


    def test_create_a_bucket_list(self):
        #test no bucketlists
        response = self.client.get('/api/v1/bucketlists/',
                                    headers=self.headers)
        self.assertIn('No bucket lists yet!', response.data.decode('utf-8'))
        #without bucket list name
        response = self.client.post('/api/v1/bucketlists/',
                    headers=self.headers)
        self.assertIn('Name of bucket list is Required',
                     response.data.decode('utf-8'))
        #with the bucket list name
        bucketlist_data = {"name": "Bucket list"}
        response = self.client.post('/api/v1/bucketlists/',
                    data=bucketlist_data,
                    headers=self.headers)
        self.assertEqual(response.status_code, 201)

        #test user cannot create the same bucketlist
        response = self.client.post('/api/v1/bucketlists/',
                    data=bucketlist_data,
                    headers=self.headers)

        self.assertEqual(response.status_code, 403)
        self.assertTrue(response.data,
                    'Sorry A similar bucket list with the same name Exists!')

    def test_delete_bucket_list(self):
        bucketlist_data = {"name": "Bucket list"}
        self.client.post('/api/v1/bucketlists/',
                    data=bucketlist_data,
                    headers=self.headers)

        #try deletig a non existent bucketlist id
        response = self.client.delete('/api/v1/bucketlists/5',
                    data=bucketlist_data,
                    headers=self.headers)
        self.assertTrue(response.data, 'No record found!')
        self.assertEqual(response.status_code, 404)

        #delete without providing an Id
        response = self.client.delete('/api/v1/bucketlists/',
                    data=bucketlist_data,
                    headers=self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.data,
                        'An id is manadatory to Delete a Bucketlist!')

        #delete an existing bucketlist
        response = self.client.delete('/api/v1/bucketlists/1',
                    data=bucketlist_data,
                    headers=self.headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Bucket list Deleted!', response.data.decode('utf-8'))

    def test_update_a_bucket_list(self):
        bucketlist_data = {"name": "Bucket list"}
        response = self.client.post('/api/v1/bucketlists/',
                    data=bucketlist_data,
                    headers=self.headers)

        new_bucketlist_data = {"name":"New bucket"}
        #test first wrong id given
        response = self.client.put('/api/v1/bucketlists/2',
                    data=new_bucketlist_data,
                    headers=self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn('No record found!', response.data.decode('utf-8'))

        response = self.client.put('/api/v1/bucketlists/1',
                    data=new_bucketlist_data,
                    headers=self.headers)
        self.assertEqual(response.status_code, 201)

    def test_add_bucket_list_items(self):
        bucketlist_data = {"name": "Bucket list"}
        response = self.client.post('/api/v1/bucketlists/',
                    data=bucketlist_data,
                    headers=self.headers)
        self.assertEqual(response.status_code, 201)

        bucket_list_items = {"item_name": "first Item",
                            "description": "I need to do this!"}
        response = self.client.post('/api/v1/bucketlists/1/items/',
                                    data=bucket_list_items,
                                    headers=self.headers)

        self.assertEqual(response.status_code, 201)

        #test cannot add to to a non-existent bucket list
        response = self.client.post('/api/v1/bucketlists/3/items/',
                                    data=bucket_list_items,
                                    headers=self.headers)
        self.assertIn('No bucket list with the ID!',
                        response.data.decode('utf-8'))

        #test cannot add the same item again
        response = self.client.post('/api/v1/bucketlists/1/items/',
                                    data=bucket_list_items,
                                    headers=self.headers)
        self.assertIn('Sorry there already exists an Item with the same name!',
                        response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 403)

        #posting without a name to the item and a description
        response = self.client.post('/api/v1/bucketlists/1/items/',
                                    headers=self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertIn('Bucket list name Required',
                     response.data.decode('utf-8'))

    def test_delete_bucket_list_item(self):
        #create a bucket list
        bucketlist_data = {"name": "Bucket list"}
        response = self.client.post('/api/v1/bucketlists/',
                    data=bucketlist_data,
                    headers=self.headers)
        #Add an item to the created bucket list
        bucket_list_items = {"item_name": "first Item",
                            "description": "I need to do this!"}
        response = self.client.post('/api/v1/bucketlists/1/items/',
                                    data=bucket_list_items,
                                    headers=self.headers)
        #delete a  non existent item
        response = self.client.delete('/api/v1/bucketlists/1/items/2',
                  headers=self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Sorry no such item!', response.data.decode('utf-8'))

        #pass a non existent Bucket list
        response = self.client.delete('/api/v1/bucketlists/2/items/1',
                 headers=self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn('No bucket list with the ID!',
                      response.data.decode('utf-8'))

        #delete existing item belonging to an existing bucket list
        response = self.client.delete('/api/v1/bucketlists/1/items/1',
                headers=self.headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Item deleted',
                     response.data.decode('utf-8'))
    def test_update_bucketlist_item(self):
        #create bucket list
        bucketlist_data = {"name": "Bucket list"}
        response = self.client.post('/api/v1/bucketlists/',
                    data=bucketlist_data,
                    headers=self.headers)

        #Add an item to the created bucket list
        bucket_list_items = {"item_name": "first Item",
                            "description": "I need to do this!"}
        self.client.post('/api/v1/bucketlists/1/items/',
                                    data=bucket_list_items,
                                    headers=self.headers)
        #update the bucket list item
        bucket_list_item = {"item_name": "update",
                            "description": "I need to do this!"}
        #update without the correct bucket list id
        response = self.client.put('/api/v1/bucketlists/2/items/1',
                                  data=bucket_list_item,
                                  headers=self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn('No bucket list with the ID!',
                        response.data.decode('utf-8'))
        #update without the wrong bucket list id
        response = self.client.put('/api/v1/bucketlists/1/items/2',
                                  data=bucket_list_item,
                                  headers=self.headers)

        self.assertEqual(response.status_code, 404)
        self.assertIn('Sorry no such item!', response.data.decode('utf-8'))

        #update with the correct details
        response = self.client.put('/api/v1/bucketlists/1/items/1',
                                  data=bucket_list_item,
                                  headers=self.headers)

        self.assertIn('Update was successfull!', response.data.decode('utf-8'))
