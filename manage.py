from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db, api
from app.models import User
from app.endpoints.user import Index, RegisterUser, LoginUser


#instantiate the app
app = create_app('testing')

#instances of Manager and Migrate classes
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(user=User)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    api.add_resource(Index, '/', 'api/v1', endpoint='index')
    api.add_resource(RegisterUser, '/auth/register', endpoint='register')
    api.add_resource(LoginUser, '/auth/login', endpoint='login')
    manager.run()
