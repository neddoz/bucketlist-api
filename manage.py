from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db, api
from app.models import User, BucketList
from app.endpoints.user import Index, RegisterUser, LoginUser
from app.endpoints.bucketlist import BucketListRepo
from app.endpoints.bucketlist_items import BucketListItemsRepo


#instantiate the app
app = create_app('development')

#instances of Manager and Migrate classes
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(User=User, BucketList=BucketList)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

api.add_resource(Index, '/', '/api/v1', endpoint='index')
api.add_resource(RegisterUser, '/auth/register', endpoint='register')
api.add_resource(LoginUser, '/auth/login', endpoint='login')
api.add_resource(BucketListItemsRepo, '/bucketlists/<id>/items/',
                        endpoint='bucketlist_items')
api.add_resource(BucketListItemsRepo, '/bucketlists/<id>/items/<item_id>')
api.add_resource(BucketListRepo, '/bucketlists/<id>',
                        endpoint='bucketlists')
api.add_resource(BucketListRepo, '/bucketlists/')

@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
