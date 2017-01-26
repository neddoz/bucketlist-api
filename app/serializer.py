from flask_restful import fields as f

bucketlistitem_serializer = {

    'id': f.Integer,
    'name': f.String,
    'done': f.Boolean,
    'description': f.String,
    'date_created': f.DateTime(dt_format='rfc822'),
    'date_modified': f.DateTime(dt_format='rfc822'),
    'bucketlist_id': f.Integer(attribute='bucketlist_id'),
}


bucketlist_serializer = {
    'id': f.Integer,
    'name': f.String,
    'date_created': f.DateTime(dt_format='rfc822'),
    'date_modified': f.DateTime(dt_format='rfc822'),
    'created_by': f.String(),
    'items': f.List(f.Nested(bucketlistitem_serializer)),
}

pagination_fields = {
    'page': f.Integer,
    'number_of_pages': f.Integer,
    'total': f.Integer,
    'next': f.String,
    'previous': f.String,
}

bucketlist_collection_serializer = {
    'pagination': f.Nested(pagination_fields),
    'bucketlists': f.List(f.Nested(bucketlist_serializer)),
}
