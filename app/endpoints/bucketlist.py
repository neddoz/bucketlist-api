from flask_restful import Resource, reqparse, abort, marshal_with
from app.models import BucketList, BucketlistItems
from app import db
from app.auth import multiple_auth
from app.serializer import bucketlist_serializer, bucketlist_collection_serializer
from app.utils import paginate
from flask import g, request
from flask import jsonify, json
import logging

class BucketListRepo(Resource):

    decorators = [multiple_auth.login_required]

    def post(self):
        #get the the bucketlist items from the post request
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str,
                            help='Name of bucket list is Required',
                            required=True)
        args = parser.parse_args()

        bucketlist_name = args["name"]

        if BucketList.query.filter_by(name=bucketlist_name).first() is not None:
             abort(403, msg='Sorry A similar bucket list with the same name Exists!')

        #create a bucketlist instance with the post data
        bucketlist = BucketList(name=bucketlist_name, user_id=g.user.id,
                                created_by=g.user.username)

        db.session.add(bucketlist)
        db.session.commit()

        return "Bucket list created succefully with the ID: %s"% bucketlist.id, 201

    @marshal_with(bucketlist_collection_serializer)
    @paginate
    def get(self):
        pass

        # bucketlists_retrieved = BucketList.query.filter_by(user_id=g.user.id).all()
        #
        # if bucketlists_retrieved:
        #     return bucketlists_retrieved, 200
        #
        # return {"message":"No bucket lists yet!"}, 200

class SingleBucketListRepo(Resource):
     decorators = [multiple_auth.login_required]

     @marshal_with(bucketlist_serializer)
     def get(self, bucketlist_id):
         bucketlist_retrieved = BucketList.query.filter_by(id=bucketlist_id, user_id=g.user.id).first()
         if bucketlist_retrieved:
             return bucketlist_retrieved
        #else not found
         abort(404, msg='Not Found!')
     def put(self, bucketlist_id):
         bucketlist_retrieved = BucketList.query.filter_by(id=bucketlist_id).first()
         if not bucketlist_retrieved:
             abort(404, msg="No record found!")

         parser = reqparse.RequestParser()
         parser.add_argument('name', type=str, help='Name of bucket list',
                             required=True)
         args = parser.parse_args()

         bucketlist_retrieved.name = args['name']

         #persist the changes in the database
         db.session.add(bucketlist_retrieved)
         db.session.commit()

         return "Update success!", 201

     def delete(self, bucketlist_id=None):

         #validation
         if not bucketlist_id:
             abort(400, msg="An id is manadatory to Delete a Bucketlist!")

         bucketlist_retrieved = BucketList.query.filter_by(id=bucketlist_id).first()
         if not bucketlist_retrieved:
             abort(404, msg="No record found!")

         #persist the changes in the database
         db.session.delete(bucketlist_retrieved)
         db.session.commit()

         return "Bucket list Deleted!", 201
