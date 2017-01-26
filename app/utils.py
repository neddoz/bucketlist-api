from flask import g, request, redirect, url_for, current_app
from flask_restful import abort
from functools import wraps
from app.models import BucketList


def paginate(f):
    @wraps(f)
    def func_wrapper(*args, **kwargs):
        page = request.args.get('page', 1, type=int)
        limit = min(request.args.get('limit',
                                     current_app.config['DEFAULT_PER_PAGE'],
                                     type=int),
                    current_app.config['MAX_PER_PAGE'])
        q = request.args.get('q')
        if q:
            bucketlists = BucketList.query.filter(BucketList.name.contains(q)).all()
            if not bucketlists:
                return {"message": "No results found!"}, 404
            else:
                return {'bucketlists': bucketlists}, 200
        page_bucketlist = BucketList.query.filter_by(user_id=g.user.id)
        page_bucketlist = page_bucketlist.paginate(page=page, per_page=limit)
        bucketlists = page_bucketlist.items
        pagination = {
            'page': page_bucketlist.page,
            'number_of_pages': page_bucketlist.pages,
            'total': page_bucketlist.total,
        }
        if page_bucketlist.has_next:
            pagination['next'] = url_for(endpoint=request.endpoint,
                                         limit=limit,
                                         page=page_bucketlist.next_num,
                                         _method='GET', q=q, _external=True,
                                         **kwargs)
        if page_bucketlist.has_prev:
            pagination['previous'] = url_for(endpoint=request.endpoint,
                                             limit=limit, page=page_bucketlist
                                             .prev_num, q=q, _method='GET',
                                             _external=True, **kwargs)
        return {'bucketlists': bucketlists, 'pagination': pagination}, 200
    return func_wrapper
