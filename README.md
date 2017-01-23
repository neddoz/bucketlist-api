
[![CircleCI](https://circleci.com/gh/neddoz/bucketlist-api.svg?style=svg)](https://circleci.com/gh/neddoz/bucketlist-api)

[![Coverage Status](https://coveralls.io/repos/github/neddoz/bucketlist-api/badge.svg?branch=develop)](https://coveralls.io/github/neddoz/bucketlist-api?branch=develop)
# bucketlist-api
BucketList Application API built using python flask framework

# Project Overview
The project employs Flask-restful for the API implementation with Postgresql
as the database.

Specification for the API is as follows:

| EndPoint                                  | Functionality                    |
| ------------------------------            |:-------------------------------: |
| POST /auth/login                          | Logs a user in                   |
| POST /auth/register                       | Register a user                  |
| POST /bucketlists/                        | Create a new bucket list         |
| GET /bucketlists/                         | List all the created bucket lists|
| GET /bucketlists/<id>                     | Get single bucket list           |
| PUT /bucketlists/<id>                     | Update this bucket list          |
| DELETE /bucketlists/<id>                  | Delete this single bucket list   |
| POST /bucketlists/<id>/items/             | Create a new item in bucket list |
| PUT /bucketlists/<id>/items/<item_id>     | Update a bucket list item        |
| DELETE /bucketlists/<id>/items/<item_id>  | Delete an item in a bucket list  |

# Installation
## Database
  The Application employs Postgresql. Firstly, is to make sure you have postgres up
  and running. Create a user **api** with a password: **password**.Next create a
  database with the name **bucketlist**. Grant All the privileges on the database
  to the user **api**.

## Application
  1. Clone the project to your preferred location on your machine
  2. create a virtual env using virtualenv.
  3. start the virtual environment to install the dependencies the project requires.
  4. Issue the following while at the root of the project from the terminal:
     ```
     pip install -r requirements.txt
     ```
  5. Next is to issue commands to start dabase migrations and set up the relations.
    One after the other issue the following commands:
    ```
    python manage.py db init

    python manage.py db migrate

    python manage.py db upgrade
    ```
  6. Next is to start the application by issuing the command **python manage.py runserver**
    The server should be running on [http://127.0.0.1:5000]

# Usage
  To use the application Postman (Google chrome extension is required).So make sure
  you have the extension added to chrome.After successfully installing the extension,
  the following steps highlight the usage:
  1. Register a user by making a post request against the url **http://127.0.0.1:5000/api/v1.0/auth/register**.
