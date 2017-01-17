from flask import jsonify
from flask_restful import Resource, reqparse, abort
from app.models import BucketList
from app import db
from app.auth import multiple_auth
from flask import g


class BucketListRepo(Resource):

    decorators = [multiple_auth.login_required]

    def post(self):
        #get the the bucketlist items from the post request
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='Name of bucket list',
                            required=True)
        args = parser.parse_args()

        bucketlist_name = args["name"]

        #validation
        if bucketlist_name is None:
            abort(400, msg='A bucket list name is required')
        if BucketList.query.filter_by(name=bucketlist_name).first() is not None:
             abort(400, msg='Sorry A similar bucket list with the same name Exists!')

        #create a bucketlist instance with the post data
        bucketlist = BucketList(name=bucketlist_name, user_id=g.user.id,
                                created_by=g.user.username)

        db.session.add(bucketlist)
        db.session.commit()

        return "Bucket list created succfull with the ID: %s"% bucketlist.id, 201
