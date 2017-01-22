from flask_restful import Resource, reqparse, abort
from flask_restful import Resource, reqparse, abort
from app.models import BucketList, BucketlistItems
from app import db
from app.auth import multiple_auth
from flask import g

class BucketListItemsRepo(Resource):
    decorators = [multiple_auth.login_required]

    def post(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('item_name', type=str,
                                        help='Bucket list name Required',
                                        required=True)
        parser.add_argument('status', type=bool, help='status of the item')
        parser.add_argument('description', type=str,
                            help='Please provide a description!',
                            required=True)
        args = parser.parse_args()

        bucketlist_retrieved = BucketList.query.get(id)

        #bucket list not found
        if not bucketlist_retrieved:
            return {"message": "No bucket list with the ID!"}, 404

        #check a user is not accessing another persons bucketlist
        if bucketlist_retrieved.user_id != g.user.id:
            return {"message": "Unathorized Access!"}, 401

        bucket_list_item_retrieved = BucketlistItems.query.filter_by(name=args['item_name']).first()
        if bucket_list_item_retrieved:
            return {"message":"Sorry there already exists an Item with the same name!"}, 403

        bucketlist_id = bucketlist_retrieved.id
        status = args['status'] or False
        new_item = BucketlistItems(name=args['item_name'],
                           done=status,
                           bucketlist_id=id,
                           description= args['description'])
        db.session.add(new_item)
        db.session.commit()

        #success message
        return {"message": "Item added successfully!", "id":new_item.id}, 201

    def put(self, id=None, item_id=None):
        if not id and not item_id:
            return "bucket list id and Item Id required for this action!"
        parser = reqparse.RequestParser()
        parser = reqparse.RequestParser()
        parser.add_argument('item_name', type=str,
                                        help='Bucket list name Required')
        parser.add_argument('status', type=bool, help='status of the item')
        parser.add_argument('description', type=str, help='status of the item')
        args = parser.parse_args()

        #Retrieve the apropriate bucket list
        bucketlist_retrieved = BucketList.query.get(id)

        #Retrieve the item
        bucket_list_item_retrieved = BucketlistItems.query.get(item_id)

        #validate the item exists:
        if not bucket_list_item_retrieved:
            return {"message": "Sorry no such item!"}, 404

        #abort if no bucket list
        if not bucketlist_retrieved:
            return {"message": "No bucket list with the ID!"}, 404

        #check a user is not accessing another persons bucketlist
        if bucketlist_retrieved.user_id != g.user.id:
            return {"message": "Unathorized Access!"}, 401

        bucket_list_item_retrieved.name = args['item_name'] or bucket_list_item_retrieved.name
        bucket_list_item_retrieved.description = args['description'] or bucket_list_item_retrieved.description
        bucket_list_item_retrieved.done = args['status'] or bucket_list_item_retrieved.done

        db.session.commit()

        return {"message":"Update was successfull!"}, 201

    def delete(self, id=None, item_id=None):

        #Retrieve the apropriate bucket list
        bucketlist_retrieved = BucketList.query.filter_by(id=id).first()

        #Retrieve the item
        bucket_list_item_retrieved = BucketlistItems.query.filter_by(id=item_id).first()

        #validate the item exists:
        if not bucket_list_item_retrieved:
            return {"message":"Sorry no such item!"}, 404

        #abort if no bucket list
        if not bucketlist_retrieved:
            return {"message":"No bucket list with the ID!"}, 404

        #check a user is not accessing another persons bucketlist
        if bucketlist_retrieved.user_id != g.user.id:
            return {"message":"Unathorized Access!"}, 401

        db.session.delete(bucket_list_item_retrieved)
        db.session.commit()

        return {"message": "Item deleted"}, 201
