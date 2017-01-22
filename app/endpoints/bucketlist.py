from flask_restful import Resource, reqparse, abort
from app.models import BucketList, BucketlistItems
from app import db
from app.auth import multiple_auth
from flask import g, request
from flask import jsonify, json


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

    def get(self, id=None):
        searchword = request.args.get('q', '') or None
        limit = request.args.get('limit', '') or 20
        kwargs = {"user_id": g.user.id}
        if searchword:
            kwargs.update({"name": searchword})
        all_bucket_lists = []
        bucketlists_retrieved = BucketList.query.filter_by(**kwargs).limit(limit).all()
        if not id:
            items = []
            for bucket_list in bucketlists_retrieved:
                #retrieve a list of items linked to each bucket list
                retrieved_items = BucketlistItems.query.filter_by(bucketlist_id=bucket_list.id).all()
                for item in retrieved_items:
                    item_dict = {"id": item.id,
                                "name":item.description,
                                "date_created":str(item.date_created),
                                "date_modified":str(item.date_modified),
                                "done":item.done}
                    items.append(item_dict)
                #return the bucket list dictinary together with its contents
                bucket_list_and_items = {"id":bucket_list.id,
                    "bucket_list_name": bucket_list.name,
                    "items":items or "No items Added!",
                    "date_created": str(bucket_list.date_created),
                    "date_modified": str(bucket_list.date_modified) or None,
                    "created_by": g.user.username}
                all_bucket_lists.append(bucket_list_and_items)
            if len(all_bucket_lists) == 0 and not searchword:
                return {"message":"No bucket lists yet!"}, 200
            if searchword and len(all_bucket_lists) == 0:
                return {"message":"No bucketlists found for the search!"}, 200
            return all_bucket_lists

        #otherwise return one bucket list for id 2given
        bucketlist_retrieved = BucketList.query.filter_by(id=id, user_id=g.user.id).first()

        if not bucketlist_retrieved:
            abort(404, msg='Not Found!')

        items = []
        retrieved_items = BucketlistItems.query.filter_by(bucketlist_id=bucketlist_retrieved.id).all()
        for item in retrieved_items:
            item_dict = {"id": item.id,
                        "name":item.description,
                        "date_created":str(item.date_created),
                        "date_modified":str(item.date_modified),
                        "done":item.done}
            items.append(item_dict)
        return {"id":bucketlist_retrieved.id,
                "bucket_list_name": bucketlist_retrieved.name,
                "items":items or "No items Added!",
                "date_created": str(bucketlist_retrieved.date_created),
                "date_modified": str(bucketlist_retrieved.date_modified) or None,
                "created_by": g.user.username}

    def put(self, id):
        bucketlist_retrieved = BucketList.query.filter_by(id=id).first()
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

    def delete(self, id=None):

        #validation
        if not id:
            abort(400, msg="An id is manadatory to Delete a Bucketlist!")

        bucketlist_retrieved = BucketList.query.filter_by(id=id).first()
        if not bucketlist_retrieved:
            abort(404, msg="No record found!")

        #persist the changes in the database
        db.session.delete(bucketlist_retrieved)
        db.session.commit()

        return "Bucket list Deleted!", 201
